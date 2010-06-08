#!/usr/bin/env python

import random
import socket
import sys

import dns.resolver
import dns.reversename

def _gethostsbyname(name):
    for rdata in dns.resolver.query(name, 'A'):
        yield rdata.address

def gethostbyname(name):
    ## NOTE: Still not entirely sure how `socket.gethostbyname`
    ## returns a single A record for an address with multiple records
    return random.choice(list(_gethostsbyname(name)))

def gethostbyname_ex(name):
    return (name, [], list(_gethostsbyname(name)))

def getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
    pass

def getfqdn(name=None):
    if name is None:
        return None
    host = gethostbyname(name)
    entry = gethostbyaddr(host)
    if entry and entry[0]:
        return entry[0]

def gethostbyaddr(address):
    name = dns.reversename.from_address(address)
    if not name:
        return None

    for entry in dns.resolver.query(name.to_text(), 'PTR'):
        # Trim the trailing dot off the name
        name = entry.to_text()[:-1]
        return (name, [], [address])

_monkeypatchable = ('gethostbyname', 'gethostbyname_ex',
        'gethostbyaddr',)
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
