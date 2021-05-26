from twisted.internet.protocol import Protocol, Factory, connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.python import failure


class Echo(Protocol):

    def __init__(self, cid, protocols):
        self._cid = cid
        self._protocols = protocols

    def connectionMade(self):
        # 连接创建是否的调用
        pass

    def dataReceived(self, data):
        self.transport.write(data)
        print(self, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("conn close.")
        try:
            del self._protocols[self._cid]
        except KeyError:
            pass


class EchoFactory(Factory):

    def __init__(self):
        self._protocols = {}
        self._cid = 0

    def gen_cid(self):
        self._cid += 1
        return self._cid

    def buildProtocol(self, addr):
        cid = self.gen_cid()
        protocol = Echo(cid, self._protocols)
        self._protocols[cid] = protocol
        return protocol


if __name__ == '__main__':
    # 8007 is the port you want to run under. Choose something >1024
    endpoint = TCP4ServerEndpoint(reactor, 8007)
    endpoint.listen(EchoFactory())
    reactor.run()

