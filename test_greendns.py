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


if __name__ == '__main__':
    unittest.main()

