import mininet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink


class SingleTopo(Topo):
    
    def build(self):
        
        self.h1 = self.addHost('h1')
        self.h2 = self.addHost('h2')

        self.s1 = self.addSwitch('s1')
        self.s2 = self.addSwitch('s2')

        self.addLink(self.h1, self.s1, bw = 100)
        self.addLink(self.s1, self.s2, bw = 2.5, delay="40ms")
        self.addLink(self.s2, self.h2, bw = 100)


net = Mininet(SingleTopo(), link=TCLink)        
net.start()
CLI(net)
net.stop()