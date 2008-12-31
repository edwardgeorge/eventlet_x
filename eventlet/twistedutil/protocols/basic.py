# Copyright (c) 2008 Denis Bilenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from twisted.protocols import basic
from twisted.internet.error import ConnectionDone
from eventlet.twistedutil.protocol import GreenTransportBase

class LineOnlyReceiver(basic.LineOnlyReceiver):

    def __init__(self, queue):
        self._queue = queue

    def connectionMade(self):
        self._queue.send(self.transport)

    def lineReceived(self, line):
        self._queue.send(line)

    def connectionLost(self, reason):
        self._queue.send_exception(reason.type, reason.value, reason.tb)

class LineOnlyReceiverTransport(GreenTransportBase):

    protocol_class = LineOnlyReceiver

    def readline(self):
        return self._wait()

    def sendline(self, line):
        self.protocol.sendLine(line)

    # iterator protocol:

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.readline()
        except ConnectionDone:
            raise StopIteration

