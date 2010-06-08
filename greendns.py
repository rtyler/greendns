#!/usr/bin/env python

import random
import socket

import dns.resolver

def _gethostsbyname(name):
    for rdata in dns.resolver.query(name, 'A'):
        yield rdata.address

def gethostbyname(name):
    return random.choice(list(_gethostsbyname(name)))

def gethostbyname_ex(name):
    return (name, [], list(_gethostsbyname(name)))

def getaddrinfo(*args, **kwargs):
    pass

_monkeypatchable = ('gethostbyname', 'gethostbyname_ex',)
