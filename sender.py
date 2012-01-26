# VOEvent sender.
# John Swinbank, <swinbank@transientskp.org>, 2011-12.

# Python standard library
import sys

# Twisted
from twisted.python import log
from twisted.python import usage
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString

# VOEvent transport protocol
from comet.tcp.protocol import VOEventSenderFactory
from comet.config.options import BaseOptions

# Constructors for messages
from comet.voevent.voevent import dummy_voevent_message

class Options(BaseOptions):
    optParameters = [
        ["host", "h", "localhost", "Host to send to."],
        ["port", "p", 8098, "Port to send to."]
    ]

    def postOptions(self):
        self["port"] = int(self["port"])

class OneShotSender(VOEventSenderFactory):
    def clientConnectionLost(self, connector, reason):
        reactor.stop()
    def clientConnectionFailed(self, connector, reason):
        log.err("Connection failed")
        reactor.stop()

if __name__ == "__main__":
    config = Options()
    config.parseOptions()

    log.startLogging(sys.stdout)
    reactor.connectTCP(
        config['host'],
        config['port'],
        OneShotSender(dummy_voevent_message(config['local_ivo']))
    )
    reactor.run()
