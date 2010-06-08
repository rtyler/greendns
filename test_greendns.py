#!/usr/bin/env python

import socket
import unittest

import greendns

class GetHostByNameTest(unittest.TestCase):
    def test_getHostByName_Ex(self):
        site = 'google.com'
        name, aliases, ips = socket.gethostbyname_ex(site)
        name, pureAliases, pureIps = greendns.gethostbyname_ex(site)
        self.assertEquals(set(ips), set(pureIps))

    def test_getHostByName(self):
        self.assertTrue(greendns.gethostbyname('google.com'))


class MonkeyPatchTests(unittest.TestCase):
    def runTest(self):
        original = socket.gethostbyname
        greendns.monkeypatch()
        self.assertEquals(greendns.gethostbyname, socket.gethostbyname)
        greendns.unmonkeypatch()
        self.assertEquals(original, socket.gethostbyname)

if __name__ == '__main__':
    unittest.main()

