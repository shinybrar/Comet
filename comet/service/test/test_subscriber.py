# Comet VOEvent Broker.
# Tests for event subscription service.

from twisted.trial import unittest
from twisted.test import proto_helpers
from comet.service import makeSubscriberService

class SubscriberServiceTestCase(unittest.TestCase):
    """Check for correct operation of the VOEvent subscriber service."""

    def setUp(self):
        self.reactor = proto_helpers.MemoryReactor()

    def test_tcp_connect(self):
        """Demonstrate that the service connects to a TCP socket."""
        self.assertEqual(len(self.reactor.tcpClients), 0)
        service = makeSubscriberService(self.reactor, "tcp:foo:8099",
                                        "ivo://foo/bar", [], [], [])
        service.startService()
        self.assertEqual(len(self.reactor.tcpClients), 1)

    def test_unix_connect(self):
        """Demonstrate that the service connects to a Unix domain socket."""
        self.assertEqual(len(self.reactor.unixClients), 0)
        service = makeSubscriberService(self.reactor, "unix:path=/dev/null",
                                        "ivo://foo/bar", [], [], [])
        service.startService()
        self.assertEqual(len(self.reactor.unixClients), 1)
