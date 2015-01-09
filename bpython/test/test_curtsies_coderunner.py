import unittest
import sys

from bpython.curtsiesfrontend.coderunner import CodeRunner, FakeOutput

class TestCodeRunner(unittest.TestCase):

    def setUp(self):
        self.orig_stdout = sys.stdout
        self.orig_stderr = sys.stderr

    def tearDown(self):
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr

    def test_simple(self):
        c = CodeRunner(request_refresh=lambda: self.orig_stdout.flush() or self.orig_stderr.flush())
        stdout = FakeOutput(c, lambda *args, **kwargs: None)
        stderr = FakeOutput(c, lambda *args, **kwargs: None)
        sys.stdout = stdout
        sys.stdout = stderr
        c.load_code('1 + 1')
        c.run_code()
        c.run_code()
        c.run_code()

    def test_exception(self):
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr
        c = CodeRunner(request_refresh=lambda: self.orig_stdout.flush() or self.orig_stderr.flush())
        def ctrlc():
            raise KeyboardInterrupt()
        stdout = FakeOutput(c, lambda x: ctrlc())
        stderr = FakeOutput(c, lambda *args, **kwargs: None)
        sys.stdout = stdout
        sys.stderr = stderr
        c.load_code('1 + 1')
        c.run_code()