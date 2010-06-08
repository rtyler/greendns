#!/usr/bin/env python

import random
import socket
import sys

import dns.resolver

def _gethostsbyname(name):
    for rdata in dns.resolver.query(name, 'A'):
        yield rdata.address

def gethostbyname(name):
    return random.choice(list(_gethostsbyname(name)))

def gethostbyname_ex(name):
    return (name, [], list(_gethostsbyname(name)))

def getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
    pass

def getfqdn(name=None):
    pass

def gethostbyaddr(address):
    pass

_monkeypatchable = ('gethostbyname', 'gethostbyname_ex',)
_monkeypatched = None

def monkeypatch():
    self = sys.modules[__name__]
    global _monkeypatched
    _monkeypatched = {}
    for name in _monkeypatchable:
        original = getattr(socket, name, None)
        new = getattr(self, name, None)
        if not original or not new:
            continue
        _monkeypatched[name] = original
        setattr(socket, name, new)

def unmonkeypatch():
    global _monkeypatched
    if not _monkeypatched:
        return
    for name, method in _monkeypatched.iteritems():
        setattr(socket, name, method)
