#!/usr/bin/env python

import socket
import unittest

import greendns

class GetHostByNameTests(unittest.TestCase):
    def test_getHostByName_Ex(self):
        site = 'google.com'
        name, aliases, ips = socket.gethostbyname_ex(site)
        name, pureAliases, pureIps = greendns.gethostbyname_ex(site)
        self.assertEquals(set(ips), set(pureIps))

    def test_getHostByName(self):
        self.assertTrue(greendns.gethostbyname('google.com'))

class GetFQDNTests(unittest.TestCase):
    def test_empty(self):
        original = socket.getfqdn()
        new = greendns.getfqdn()
        self.assertEquals(new, original)

    def test_eventletnet(self):
        original = socket.getfqdn('eventlet.net')
        new = greendns.getfqdn('eventlet.net')
        self.assertEquals(new, original)

class GetAddrInfoTests(unittest.TestCase):
    def runTest(self):
        original = socket.getaddrinfo('www.python.org', 80, 0, 0, socket.SOL_TCP)
        new = greendns.getaddrinfo('www.python.org', 80, 0, 0, socket.SOL_TCP)
        self.assertEquals(new, original)

class GetHostByAddr(unittest.TestCase):
    def test_localhost(self):
        original = socket.gethostbyaddr('127.0.0.1')
        new = greendns.gethostbyaddr('127.0.0.1')
        self.assertEquals(new, original)

    def test_google(self):
        original = socket.gethostbyaddr('74.125.19.99')
        new = greendns.gethostbyaddr('74.125.19.99')
        self.assertEquals(new, original)


class MonkeyPatchTests(unittest.TestCase):
    def runTest(self):
        original = socket.gethostbyname
        greendns.monkeypatch()
        self.assertEquals(greendns.gethostbyname, socket.gethostbyname)
        greendns.unmonkeypatch()
        self.assertEquals(original, socket.gethostbyname)

if __name__ == '__main__':
    unittest.main()

