#!/usr/bin/env python

import random
import socket
import sys

import dns.ipv6
import dns.resolver
import dns.reversename

def _records(name, mode):
    for rdata in dns.resolver.query(name, mode):
        yield rdata.address

def _Arecords(name):
    return _records(name, 'A')

def _AAAArecords(name):
    return _records(name, 'AAAA')

def gethostbyname(name):
    ## NOTE: Still not entirely sure how `socket.gethostbyname`
    ## returns a single A record for an address with multiple records
    return random.choice(list(_Arecords(name)))

def gethostbyname_ex(name):
    return (name, [], list(_Arecords(name)))

def getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
    info = []
    socktype = socktype or socket.SOCK_STREAM
    proto = proto or socket.IPPROTO_TCP

    try:
        # Check to see if this is really an IP address
        family = dns.inet.af_for_address(host)
        return [(family, socktype, proto, '', (host, port))]
    except ValueError:
        pass

    if family == 0 or family == socket.AF_INET:
        for record in _Arecords(host):
            entry = (socket.AF_INET, socktype, proto, '', (record, port))
            info.append(entry)

    if not socket.has_ipv6 or not family == socket.AF_INET6:
        return info

    for record in _AAAArecords(host):
        entry = (socket.AF_INET6, socktype, proto, '', (record, port))
        info.append(entry)

    return info

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
        'gethostbyaddr', 'getaddrinfo', 'getfqdn',)
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
