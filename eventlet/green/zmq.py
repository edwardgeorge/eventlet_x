import errno

_zmq = __import__('zmq')
globals().update(dict((k, v) for k, v in _zmq.__dict__.iteritems()
    if not k.startswith('__')))
from eventlet.hubs import trampoline

_zmq_Socket = Socket

class Socket(_zmq_Socket):
    def send(self, data, flags=0, copy=True):
        raise_noblock = flags & NOBLOCK
        flags = flags | NOBLOCK
        while True:
            try:
                return super(Socket, self).send(data, flags, copy)
            except IOError, e:
                print 'ioerror', e
                if e.errno != errno.EAGAIN or raise_noblock:
                    raise
            print 'trampolining'
            trampoline(self, write=True)


    def recv(self, flags=0, copy=True):
        raise_noblock = flags & NOBLOCK
        flags = flags | NOBLOCK
        while True:
            try:
                return super(Socket, self).recv(flags, copy)
            except IOError, e:
                print 'ioerror', e
                if e.errno != errno.EAGAIN or raise_noblock:
                    raise
            print 'trampolining'
            trampoline(self, write=True)
