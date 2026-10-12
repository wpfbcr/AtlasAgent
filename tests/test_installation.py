"""Installer regression tests; all writes stay inside temporary directories."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="atlas installation ")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base / "repo with spaces"
        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
        shutil.copytree(ROOT / "skills", self.repo / "skills")
        self.user = self.base / "isolated user"
        self.user.mkdir()
        self.rc = self.user / ".zshrc"
        self.rc.write_text("# unrelated user config\n")
        self.dest = self.user / ".cursor/skills"
        self.env = os.environ.copy()
        self.env.update(ATLAS_USER_HOME=str(self.user), ATLAS_ROOT=str(self.repo))

    def run_install(self, *args):
        return subprocess.run(
            ["bash", str(self.repo / "scripts/install.sh"), *args],
            env=self.env, capture_output=True, text=True, timeout=20,
        )

    def existing_skill(self, name="weather", dest=None):
        target = (dest or self.dest) / name
        target.mkdir(parents=True)
        (target / "custom.txt").write_text("user content\n")
        return target

    def fake_tool(self, name, body):
        bin_dir = self.base / "bin"
        bin_dir.mkdir(exist_ok=True)
        tool = bin_dir / name
        tool.write_text("#!/bin/sh\n" + body + "\n")
        tool.chmod(0o755)
        self.env["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]

    def assert_no_stage(self):
        self.assertEqual(list(self.dest.glob(".atlas-stage.*")), [])

    def test_fresh_install_and_repeat_are_idempotent(self):
        first = self.run_install("cursor")
        self.assertEqual(first.returncode, 0, first.stderr)
        installed = sorted(p.name for p in self.dest.iterdir())
        expected = sorted(p.name for p in (self.repo / "skills").iterdir())
        self.assertEqual(installed, expected)
        before = (self.dest / "weather/SKILL.md").stat().st_mtime_ns
        rc_before = self.rc.read_text()
        second = self.run_install("cursor")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((self.dest / "weather/SKILL.md").stat().st_mtime_ns, before)
        self.assertEqual(self.rc.read_text(), rc_before)
        self.assertFalse((self.dest / ".atlas-backups").exists())
        self.assert_no_stage()

    def test_conflict_preserves_every_target_and_shell_config(self):
        existing = self.existing_skill()
        result = self.run_install("cursor")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--overwrite", result.stderr)
        self.assertEqual((existing / "custom.txt").read_text(), "user content\n")
        self.assertFalse((self.dest / "atlas-agent").exists())
        self.assertEqual(self.rc.read_text(), "# unrelated user config\n")
        self.assert_no_stage()

    def test_all_preflights_later_agents_before_any_install(self):
        existing = self.existing_skill(dest=self.user / ".agents/skills")
        result = self.run_install("all")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((existing / "custom.txt").exists())
        self.assertFalse(self.dest.exists())
        self.assertFalse((self.user / ".claude").exists())
        self.assertEqual(self.rc.read_text(), "# unrelated user config\n")

    def test_overwrite_retains_exact_old_content_in_unique_backups(self):
        existing = self.existing_skill()
        result = self.run_install("cursor", "--overwrite")
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.dest / ".atlas-backups").glob("weather.*/weather"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "custom.txt").read_text(), "user content\n")
        self.assertIn(str(backups[0]), result.stdout)
        self.assertFalse((existing / "custom.txt").exists())
        self.assertEqual((existing / "SKILL.md").read_bytes(), (self.repo / "skills/weather/SKILL.md").read_bytes())
        (existing / "custom.txt").write_text("second customization\n")
        second = self.run_install("cursor", "--overwrite")
        self.assertEqual(second.returncode, 0, second.stderr)
        backups = list((self.dest / ".atlas-backups").glob("weather.*/weather"))
        self.assertEqual(len(backups), 2)
        self.assertEqual({(b / "custom.txt").read_text() for b in backups}, {"user content\n", "second customization\n"})
        self.assert_no_stage()

    def test_copy_failure_preserves_previous_skill(self):
        existing = self.existing_skill("atlas-agent")
        self.fake_tool("cp", "exit 9")
        result = self.run_install("cursor", "--overwrite")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((existing / "custom.txt").read_text(), "user content\n")
        self.assertFalse((self.dest / ".atlas-backups").exists())
        self.assert_no_stage()

    def test_final_move_failure_restores_previous_skill(self):
        existing = self.existing_skill("atlas-agent")
        self.fake_tool("mv", 'case "$2" in *"/.atlas-stage."*) exit 9 ;; esac\nexec /bin/mv "$@"')
        result = self.run_install("cursor", "--overwrite")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((existing / "custom.txt").read_text(), "user content\n")
        self.assertFalse((existing / "SKILL.md").exists())
        self.assert_no_stage()

    def test_symlink_conflict_keeps_external_target_intact(self):
        external = self.base / "external skill"
        external.mkdir()
        (external / "custom.txt").write_text("external content")
        self.dest.mkdir(parents=True)
        (self.dest / "weather").symlink_to(external, target_is_directory=True)
        blocked = self.run_install("cursor")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertTrue((self.dest / "weather").is_symlink())
        replaced = self.run_install("cursor", "--overwrite")
        self.assertEqual(replaced.returncode, 0, replaced.stderr)
        self.assertEqual((external / "custom.txt").read_text(), "external content")
        backup = next((self.dest / ".atlas-backups").glob("weather.*/weather"))
        self.assertTrue(backup.is_symlink())
        self.assertFalse((self.dest / "weather").is_symlink())

    def test_invalid_options_do_not_write(self):
        for args in [("bogus",), ("cursor", "--overwite")]:
            with self.subTest(args=args):
                result = self.run_install(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.dest.exists())
                self.assertEqual(self.rc.read_text(), "# unrelated user config\n")

    def run_cli(self, *args):
        return subprocess.run(
            ["bash", str(self.repo / "scripts/atlas-agent"), "install", *args],
            env=self.env, text=True, capture_output=True, timeout=20,
        )

    def test_cli_forwards_overwrite_and_does_not_install_dependencies(self):
        self.existing_skill()
        self.fake_tool("python3", "exit 0")
        blocked = self.run_cli("--agent=cursor")
        self.assertNotEqual(blocked.returncode, 0)
        success = self.run_cli("--agent=cursor", "--overwrite")
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertTrue((self.dest / "weather/SKILL.md").exists())
        self.assertEqual(len(list((self.dest / ".atlas-backups").glob("weather.*/weather"))), 1)

    def test_safe_and_dry_run_do_not_modify_anything(self):
        self.existing_skill()
        for flag in ["--safe", "--dry-run"]:
            with self.subTest(flag=flag):
                result = self.run_cli("--agent=cursor", "--overwrite", flag)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((self.dest / "weather/custom.txt").exists())
                self.assertFalse((self.dest / "atlas-agent").exists())
                self.assertFalse((self.dest / ".atlas-backups").exists())
                self.assertEqual(self.rc.read_text(), "# unrelated user config\n")

    def test_no_env_keeps_shell_configuration_unchanged(self):
        original = self.rc.read_text()
        result = self.run_install("cursor", "--no-env")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rc.read_text(), original)
        self.assertTrue((self.dest / "weather/SKILL.md").exists())

    def test_safe_no_env_instructions_propagate_the_option(self):
        result = self.run_cli("--agent=cursor", "--env=none", "--safe")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--no-env", result.stdout)
        self.assertFalse(self.dest.exists())

    def test_cli_rejects_invalid_agent_and_typo(self):
        for args in [("--agent=bogus", "--dry-run"), ("--overwite",)]:
            result = self.run_cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.dest.exists())


class DocumentationTests(unittest.TestCase):
    def test_update_and_agent_commands_run_with_a_space_in_root(self):
        with tempfile.TemporaryDirectory(prefix="atlas docs ") as folder:
            root = Path(folder)
            scripts = root / "scripts"
            scripts.mkdir()
            log = root / "calls.txt"
            (scripts / "atlas-agent").write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$ATLAS_TEST_LOG"\n')
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name in ["git", "pip3"]:
                tool = bin_dir / name
                tool.write_text("#!/bin/sh\nexit 0\n")
                tool.chmod(0o755)
            env = os.environ.copy()
            env.update(ATLAS_ROOT=str(root), ATLAS_TEST_LOG=str(log), PATH=str(bin_dir) + os.pathsep + env["PATH"])
            commands = []
            for name in ["docs/update.md", "AGENTS.md"]:
                commands.extend(re.findall(r"```bash\n(.*?)```", (ROOT / name).read_text(), re.S))
            skill = (ROOT / "skills/atlas-agent/SKILL.md").read_text()
            commands.extend(re.findall(r"Verify: `(.*?)`", skill))
            for command in commands:
                with self.subTest(command=command):
                    syntax = subprocess.run(["bash", "-n"], input=command, capture_output=True, text=True)
                    self.assertEqual(syntax.returncode, 0, syntax.stderr)
                    result = subprocess.run(["bash", "-eu"], input=command, env=env, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stderr)
            calls = log.read_text().splitlines()
            self.assertIn("install --env=auto --agent=all", calls)
            self.assertIn("install --env=auto --agent=all --overwrite", calls)
            self.assertIn("doctor", calls)
            self.assertIn("check-update", calls)


if __name__ == "__main__":
    unittest.main()
