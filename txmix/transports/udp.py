
from __future__ import print_function

from zope.interface import implementer
from twisted.internet.protocol import DatagramProtocol

from txmix import IMixTransport


@implementer(IMixTransport, IConsumer, IPushProducer)
class UDPTransport(DatagramProtocol):
    """
    implements the IMixTransport interface
    """
    name = "udp"

    def __init__(self, reactor):
        self.reactor = reactor
        self.consumer = None

    def make_connection(self, addr, nodeProtocol):
        """
        make this transport begin listening on the specified interface and UDP port
        interface must be an IP address
        """
        self.consumer = nodeProtocol
        interface, port = addr
        self.reactor.listenUDP(port, self, interface=interface)

    def send(self, addr, message):
        """
        send message to addr
        where addr is a 2-tuple of type: (ip address, UDP port)
        """
        self.transport.write(message, addr)

    # IConsumer methods

    def registerProducer(self, producer, streaming):
        assert streaming
        self.consumer = producer

    def unregisterProducer(self):
        pass

    def write(self, data):
        addr, message = data
        self.send(addr, message)

    # IPushProducer methods

    def pauseProducing(self):
        pass

    def resumeProducing(self):
        pass

    def datagramReceived(self, datagram, addr):
        """
        i am called by the twisted reactor when our transport receives a UDP packet
        """
        self.consumer.write(datagram)
