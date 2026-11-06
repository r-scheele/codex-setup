import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('quality', Path(__file__).with_name('quality.py'))
quality = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        (self.root / 'source.py').write_text('original')

    def snapshot(self):
        return quality.snapshot(self.root, [])

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)

    def test_regular_files_content_mode_and_deletion(self):
        before = self.snapshot()
        (self.root / 'source.py').chmod(0o755)
        self.assertNotEqual(before, self.snapshot())
        before = self.snapshot()
        (self.root / 'source.py').write_text('changed')
        self.assertNotEqual(before, self.snapshot())
        (self.root / 'other.py').write_text('other')
        before = self.snapshot()
        (self.root / 'source.py').unlink()
        self.assertNotEqual(before, self.snapshot())

    def test_internal_file_link_binds_target_bytes_and_link_text(self):
        link = self.root / 'alias'
        link.symlink_to('source.py')
        before = self.snapshot()
        (self.root / 'source.py').write_text('changed')
        self.assertNotEqual(before, self.snapshot())
        before = self.snapshot()
        link.unlink()
        link.symlink_to('./source.py')
        self.assertNotEqual(before, self.snapshot())

    def test_git_directory_link_binds_selected_target_bytes(self):
        self.git('init', '-q')
        target = self.root / 'instructions'
        target.mkdir()
        (target / 'SKILL.md').write_text('one')
        (self.root / 'alias').symlink_to('instructions', target_is_directory=True)
        self.git('add', '.')
        before = self.snapshot()
        (target / 'SKILL.md').write_text('two')
        self.assertNotEqual(before, self.snapshot())
        (target / 'new.md').write_text('untracked source')
        before = self.snapshot()
        (target / 'new.md').write_text('changed untracked source')
        self.assertNotEqual(before, self.snapshot())

    def test_retargeting_a_link_changes_snapshot(self):
        for name in ['one', 'two']:
            (self.root / name).mkdir()
            (self.root / name / 'file').write_text('same')
        link = self.root / 'alias'
        link.symlink_to('one')
        before = self.snapshot()
        link.unlink()
        link.symlink_to('two')
        self.assertNotEqual(before, self.snapshot())

    def test_external_file_directory_and_indirect_link_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (outside / 'file').write_text('external')
        for target in [outside / 'file', outside]:
            with self.subTest(target=target):
                link = self.root / 'alias'
                link.symlink_to(target)
                with self.assertRaisesRegex(ValueError, 'escapes source root'):
                    self.snapshot()
                link.unlink()
        (self.root / 'alias').symlink_to(outside)
        (self.root / 'indirect').symlink_to('alias/file')
        with self.assertRaisesRegex(ValueError, 'escapes source root'):
            self.snapshot()

    def test_dangling_and_cyclic_links_rejected(self):
        link = self.root / 'alias'
        link.symlink_to('missing')
        with self.assertRaisesRegex(ValueError, 'broken or cyclic'):
            self.snapshot()
        link.unlink()
        link.symlink_to('alias')
        with self.assertRaisesRegex(ValueError, 'broken or cyclic'):
            self.snapshot()

    def test_ignored_target_rejected_unless_explicitly_selected(self):
        self.git('init', '-q')
        (self.root / '.gitignore').write_text('ignored.py\n')
        (self.root / 'ignored.py').write_text('ignored')
        (self.root / 'alias').symlink_to('ignored.py')
        self.git('add', '.')
        with self.assertRaisesRegex(ValueError, 'not covered'):
            self.snapshot()
        before = quality.snapshot(self.root, ['ignored.py'])
        (self.root / 'ignored.py').write_text('changed')
        self.assertNotEqual(before, quality.snapshot(self.root, ['ignored.py']))

    def test_uncovered_directory_and_submodule_still_rejected(self):
        self.git('init', '-q')
        (self.root / 'empty').mkdir()
        (self.root / 'alias').symlink_to('empty')
        self.git('add', '.')
        with self.assertRaisesRegex(ValueError, 'not covered'):
            self.snapshot()
        (self.root / 'alias').unlink()
        self.git('rm', '--cached', 'alias')
        (self.root / 'module').mkdir()
        self.git('update-index', '--add', '--cacheinfo', '160000,' + '1' * 40 + ',module')
        with self.assertRaisesRegex(ValueError, 'submodule/directory'):
            self.snapshot()

    def test_freshness_check_detects_link_target_change(self):
        (self.root / 'alias').symlink_to('source.py')
        candidate = {'root': str(self.root), 'extra_inputs': [], 'source': self.snapshot()}
        quality.fresh(candidate)
        (self.root / 'source.py').write_text('later')
        with self.assertRaisesRegex(ValueError, 'source changed'):
            quality.fresh(candidate)


if __name__ == '__main__':
    unittest.main()
