#!/usr/bin/python3

import unittest
import subprocess
import os
import tempfile
import time

class TestConfused(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.mountpoint = tempfile.TemporaryDirectory()
        self.fake = tempfile.TemporaryDirectory()
        self.test_dirs = [self.root, self.mountpoint, self.fake]
        self.popen = subprocess.Popen(
            ['./confused.py', self.root.name, self.mountpoint.name, self.fake.name])
        with open(os.path.join(self.root.name, 'ready.txt'), 'w') as f:
            f.write('')
        for _ in range(5):
            if os.path.exists(os.path.join(self.mountpoint.name, 'ready.txt')):
                os.remove(os.path.join(self.mountpoint.name, 'ready.txt'))
                return
            time.sleep(1)
        raise

    def tearDown(self):
        self.popen.terminate()
        self.popen.wait()
        for test_dir in self.test_dirs:
            test_dir.cleanup()

    def test_sanity(self):
        overridden_file = 'file.txt'
        with open(os.path.join(self.root.name, overridden_file), 'w') as f:
            f.write('realrealreal')
        with open(os.path.join(self.fake.name, overridden_file), 'w') as f:
            f.write('fake')
        with open(os.path.join(self.mountpoint.name, overridden_file)) as f:
            self.assertEqual(f.read(), 'fake')


if __name__ == '__main__':
    unittest.main()
