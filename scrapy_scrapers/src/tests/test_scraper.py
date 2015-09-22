import os
import subprocess
import unittest
import SimpleHTTPServer
import SocketServer

from spiders.scrapers import CustomScraper


class TestScraper(unittest.TestCase):

    def setUp(self):
        self.proc = subprocess.Popen("cd test_pages; python -m SimpleHTTPServer 7999", shell=True)

    def tearDown(self):
        os.kill(self.proc.pid, 9)

    def test_something(self):
        assert 1
