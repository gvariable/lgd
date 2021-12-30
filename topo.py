from mininet.topo import Topo

class AwesomeBottleneckTopo(Topo):
    """Build Awesome Topo for Computer Network Design"""

    def build(self, client_num=3, server_num=3):

        #  awesome_client1                                    awesome_server1(5Mbps)
        #                  \ 40Mbps                 40Mbps   /
        #  awesome_client2 --------- s1 --------- s2 -------- awesome_server2(30Mbps)
        #                  /          35Mbps(20ms)           \
        #  awesome_client3                                    awesome_server3(20Mbps)

        # TODO(gpl): add awesome topo
        self.clients = [self.addHost(f'h{i + 1}')
                        for i in range(client_num)]
        self.servers = [self.addHost(f'n{i + 1}')
                        for i in range(server_num)]

        self.s1 = self.addSwitch('awesome-s1')
        self.s2 = self.addSwitch('awesome-s2')

        linkops = dict(bw=35, delay='5ms',
                       max_queue_size=1000, use_htb=True)
        self.addLink(self.s1, self.s2, **linkops)
        print("clients:", self.clients)
        for client in self.clients:
            print(client)
            linkops = dict(bw=40, max_queue_size=1000, use_htb=True)
            self.addLink(client, self.s1, **linkops)

        for server in self.servers:
            linkops = dict(bw=40, max_queue_size=1000, use_htb=True)
            self.addLink(server, self.s2, **linkops)

class AwesomeLongFatTopo(Topo):

    def build(self):

        self.client = self.addHost("h1")
        self.server = self.addHost("n1")
        self.s = self.addSwitch("s1")

        client_ops = dict(bw=1000, delay="20ms", max_queue_size=1000, loss=10, use_htb=True)
        server_ops = dict(bw=1000, delay="5ns", max_queue_size=1000, use_htb=True)
        self.addLink(self.client, self.s, **client_ops)
        self.addLink(self.server, self.s, **server_ops)

        client_ops = dict(bw=100, delay="20ms", max_queue_size=1000, loss=10, use_htb=True)