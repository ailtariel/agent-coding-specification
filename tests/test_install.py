import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts/install.py"
spec = importlib.util.spec_from_file_location("installer", MODULE)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        self.home = self.root / "user with spaces"
        self.codex = self.home / ".codex"
        self.state = self.home / ".agents/agent-coding-specification"
        self.write(self.repo / "AI-coding-specification/README.md", "Rules\n")
        self.write(self.repo / "AGENTS.global.template.md", "Read {{SPECIFICATION_PATH}}/README.md\n")
        self.write(self.repo / "skills/openai-docs/SKILL.md", "---\nname: openai-docs\ndescription: Docs\n---\nLocal\n")
        self.write(self.repo / "skills/web-project/SKILL.md", "---\nname: web-project\ndescription: Router\n---\n")
        self.write(self.repo / "skills/web-project/vue/SKILL.md", "---\nname: vue\ndescription: Vue\n---\n")
        self.write(self.repo / "skills/system-overrides.json", '["openai-docs"]')
        self.write(self.codex / "config.toml", '# Keep this comment\nmodel = "existing"\n[features]\nexample = true\n')
        self.write(self.codex / "AGENTS.md", "# Personal\n\nKeep my preference.\n")
        self.write(self.home / ".agents/skills/unrelated/SKILL.md", "---\nname: unrelated\n---\nKeep\n")
        self.root_patch = patch.object(installer, "ROOT", self.repo)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.env_patch = patch.dict(os.environ, {}, clear=False)
        self.env_patch.start()
        os.environ.pop("CODEX_HOME", None)
        self.addCleanup(self.env_patch.stop)

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def run_install(self, *args):
        with patch.object(sys, "argv", [str(MODULE), "--home", str(self.home), *map(str, args)]), contextlib.redirect_stdout(io.StringIO()):
            return installer.main()

    def test_install_idempotence_and_preservation(self):
        self.assertEqual(self.run_install(), 0)
        first = installer.fingerprint(self.home)
        self.assertEqual(self.run_install(), 0)
        self.assertEqual(first, installer.fingerprint(self.home))
        self.assertEqual(self.run_install("--check"), 0)
        self.assertIn("Keep my preference", installer.text(self.codex / "AGENTS.md"))
        self.assertIn("Keep this comment", installer.text(self.codex / "config.toml"))
        data = tomllib.loads(installer.text(self.codex / "config.toml"))
        self.assertEqual(data["model"], "existing")
        self.assertFalse(data["skills"]["config"][0]["enabled"])
        self.assertTrue((self.home / ".agents/skills/unrelated/SKILL.md").exists())

    def test_preview_has_no_target_writes(self):
        before = installer.fingerprint(self.home)
        self.assertEqual(self.run_install("--dry-run"), 0)
        self.assertEqual(before, installer.fingerprint(self.home))

    def test_update_and_restore_existing_skill(self):
        target = self.home / ".agents/skills/openai-docs/SKILL.md"
        self.write(target, "---\nname: openai-docs\n---\nOriginal\n")
        old_agents = (self.codex / "AGENTS.md").read_bytes()
        old_config = (self.codex / "config.toml").read_bytes()
        self.run_install()
        backup = next((self.state / "backups").iterdir())
        self.assertEqual(self.run_install("--restore", backup), 0)
        self.assertIn("Original", installer.text(target))
        self.assertEqual((self.codex / "AGENTS.md").read_bytes(), old_agents)
        self.assertEqual((self.codex / "config.toml").read_bytes(), old_config)

    def test_restore_refuses_to_discard_later_user_edits(self):
        self.run_install()
        backup = next((self.state / "backups").iterdir())
        self.write(self.codex / "AGENTS.md", "Later user change")
        with self.assertRaisesRegex(ValueError, "Changed since"):
            self.run_install("--restore", backup)
        self.assertEqual(installer.text(self.codex / "AGENTS.md"), "Later user change")

    def test_override_agents_and_custom_codex_home(self):
        custom = self.root / "custom codex"
        self.write(custom / "AGENTS.override.md", "Override preference\n")
        self.run_install("--codex-home", custom)
        self.assertIn("Override preference", installer.text(custom / "AGENTS.override.md"))
        self.assertIn("BEGIN agent-coding", installer.text(custom / "AGENTS.override.md"))
        self.assertNotIn("BEGIN agent-coding", installer.text(self.codex / "AGENTS.md"))

    def test_existing_skill_config_is_updated_without_duplicate(self):
        path = self.codex / "skills/.system/openai-docs/SKILL.md"
        content = '# Preserved\n[[skills.config]]\npath = ' + json.dumps(path.as_posix()) + '\nenabled = true\n[other]\nvalue = 1\n'
        self.write(self.codex / "config.toml", content)
        self.run_install()
        parsed = tomllib.loads(installer.text(self.codex / "config.toml"))
        self.assertEqual(len(parsed["skills"]["config"]), 1)
        self.assertFalse(parsed["skills"]["config"][0]["enabled"])
        self.assertEqual(parsed["other"]["value"], 1)

    def test_drift_is_detected(self):
        self.run_install()
        self.write(self.home / ".agents/skills/web-project/vue/SKILL.md", "---\nname: vue\n---\nModified\n")
        self.assertEqual(self.run_install("--check"), 1)

    def test_partial_failure_rolls_back_all_touched_targets(self):
        old_agents = (self.codex / "AGENTS.md").read_bytes()
        real_copy = installer.copy
        failed = False

        def failing_copy(source, target):
            nonlocal failed
            if target == self.codex / "config.toml" and not failed:
                failed = True
                raise OSError("Injected copy failure")
            real_copy(source, target)

        with patch.object(installer, "copy", failing_copy):
            with self.assertRaisesRegex(OSError, "Injected"):
                self.run_install()
        self.assertEqual((self.codex / "AGENTS.md").read_bytes(), old_agents)
        self.assertFalse((self.home / ".agents/skills/openai-docs").exists())
        self.assertEqual(tomllib.loads(installer.text(self.codex / "config.toml"))["model"], "existing")

    def test_link_outside_home_is_not_overwritten(self):
        destination = self.home / ".agents/skills/openai-docs"
        outside = self.root / "outside"
        outside.mkdir()
        try:
            destination.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation unavailable for this user")
        with self.assertRaisesRegex(ValueError, "linked installation"):
            self.run_install()
        self.assertTrue(destination.is_symlink())

    def test_exact_legacy_template_migrates_preferences(self):
        previous = "# Global Agent Working Rules\n\n## User Preferences\n\n- Add personal global preferences here.\n\n## Canonical Coding Specification\n\n`C:/old/AI-coding-specification/`\n\nGenerated policy\n"
        self.write(self.repo / "scripts/legacy-global-agents.template.md", previous)
        customized = previous.replace("- Add personal global preferences here.", "- Prefer Chinese replies.").replace("C:/old", "/home/me/old")
        self.write(self.codex / "AGENTS.md", customized)
        self.run_install()
        result = installer.text(self.codex / "AGENTS.md")
        self.assertIn("Prefer Chinese replies", result)
        self.assertNotIn("Generated policy", result)
        self.assertNotIn("/home/me/old", result)


if __name__ == "__main__":
    unittest.main()
