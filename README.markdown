Green DNS
===========

Just a simple module built around [dnspython](http://www.dnspython.org) that
monkey-patches the standard library for "green" DNS support.

Best used with [Eventlet](http://eventlet.net)


Suggested use (with Eventlet):

    import eventlet
    greendns = eventlet.import_patched('greendns')
    greendns.monkeypatch(module=greendns)
