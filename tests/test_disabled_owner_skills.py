import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DisabledSkillsTest(unittest.TestCase):
    def test_refusal_preserves_files(self):
        scripts = list((ROOT / 'skills/printing-press-import/references').glob('*.sh'))
        scripts += list((ROOT / 'skills/printing-press-reprint/references').glob('*.sh'))
        self.assertEqual(len(scripts), 5)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'outside').mkdir()
            (base / 'outside/keep.txt').write_text('keep me')
            (base / 'staging').mkdir()
            (base / 'staging/research.json').write_text('{"researched_at":"invalid"}')
            (base / 'link').symlink_to(base / 'outside', target_is_directory=True)

            # Finder may add its metadata concurrently; compare all other entries.
            def snapshot():
                return {str(p.relative_to(base)): (
                    'link:' + str(p.readlink()) if p.is_symlink() else
                    hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'dir'
                ) for p in base.rglob('*') if p.name != '.DS_Store'}

            before = snapshot()
            for script in scripts:
                for value in ('valid-name', '../../outside', str(base / 'outside'),
                              'link', "'; raise Exception('injection'); #", ''):
                    with self.subTest(script=script.name, value=value):
                        result = subprocess.run(
                            ['/bin/sh', str(script), str(base / 'staging'), value],
                            cwd=base, env={'PATH': '/usr/bin:/bin'},
                            capture_output=True, text=True, timeout=5)
                        self.assertEqual(result.returncode, 78)
                        self.assertIn('BLOCKED:', result.stderr)
                        self.assertEqual(snapshot(), before)


if __name__ == '__main__':
    unittest.main()
