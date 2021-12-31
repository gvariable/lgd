import logging
import mininet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import time
import subprocess
from gym_lgd.envs.topo import *


awesome_logger = logging.getLogger('awesomework')
awesome_logger.setLevel(logging.INFO)
awesome_logger.debug("AwesomeTopo started!")


class BottleneckBackend(object):
    def __init__(self, topo: AwesomeBottleneckTopo=AwesomeBottleneckTopo(), debug=False) -> None:
        self.net = Mininet(topo, link=TCLink)
        self.clients = self.net.topo.clients
        self.servers = self.net.topo.servers

        self.bws, self.rtrys, self.cwnds, self.rtts, self.netpwrs = [], [], [], [], []

        self.debug = debug
        self.net.start()

        # TCP Server iperf output table

        #################################################################
        # Interval            Transfer    Bandwidth       Reads   Dist  #
        #################################################################

        # UDP Server iperf output table
        ################################################################################################################
        # Interval            Transfer     Bandwidth        Jitter   Lost/Total  Latency avg/min/max/stdev PPS  NetPwr #
        ################################################################################################################

        for idx, server in enumerate(self.servers):
            if idx != len(self.servers) - 1:
                self.net.get(server).cmd(
                    f"iperf -s -e -i 1 > /tmp/awesome_tcp_{server}.log &")
            else:
                self.net.get(server).cmd(
                    f"iperf -s -e -u -i 1 > /tmp/awesome_udp_{server}.log &")

        self.take_measurements()
        CLI(self.net)
        self.clean()

    def send_tcp_package(self, t=50, mean="20M", deviation="2M", cong_alg=None):
        """Send tcp package from tcp client to tcp server.

        TCP Client iperf output table:

            ################################################################################################
            #  Interval            Transfer     Bandwidth       Write/Err  Rtry     Cwnd/RTT        NetPwr #
            ################################################################################################

        Args:
            t (int, optional): time in seconds to listen for new traffic connections. Defaults to 10.
        """
        # TODO(gpl): bandwidth, ttl, congestion algorithms
        for idx, (client, server) in enumerate(zip(self.clients, self.servers)):
            if idx != len(self.servers) - 1:
                if cong_alg:
                    self.net.get(client).cmd(f"iperf -c {self.net.get(server).IP()} -i 1 -b {mean},{deviation} -e -t {t} -Z {cong_alg}> /tmp/awesome_tcp_{client}.log &")
                else:
                    self.net.get(client).cmd(f"iperf -c {self.net.get(server).IP()} -i 1 -b {mean},{deviation} -e -t {t} > /tmp/awesome_tcp_{client}.log &")

    def send_udp_datagram(self, t=10):
        """Send udp datagram from udp client to udp server.

        UDP Client iperf output table:
            ##################################################################
            # Interval            Transfer     Bandwidth      Write/Err  PPS #
            ##################################################################

        Args:
            t (int, optional): time in seconds to listen for new traffic connections. Defaults to 10.
        """
        for client in self.clients:
            self.net.get(client).cmd(
                f"iperf -c {self.net.get(self.servers[-1]).IP()} -u -i 1 -t {t} -e > /tmp/awesome_udp_{client}.log &")

    def take_measurements(self, cong_alg=None):
        
        subprocess.run("sudo rm -rf /tmp/*.log", shell=True)
        self.send_tcp_package(cong_alg=cong_alg)
        logging.debug("sleeping 5 secs for waiting tcp transmitting")
        time.sleep(5)


        for client in self.clients[:-1]:
            with open(f"/tmp/awesome_tcp_{client}.log") as f:
                for line in f.readlines():
                    if "bits/sec" in line:
                        line = line.replace("-", ' ')
                        line = line.replace("/", ' ')
                        fields = line.strip().split()
                        self.bws.append(float(fields[7]))
                        self.rtrys.append(float(fields[12]))
                        self.cwnds.append(int(fields[13][:-1])) # K
                        self.rtts.append(int(fields[14]))
                        self.netpwrs.append(float(fields[-1]))
        

    def clean(self):
        if not self.debug:
            subprocess.run('sudo rm -rf /tmp/*.log', shell=True)

        self.net.stop()
        subprocess.run('sudo mn -c', shell=True)


class LongFatBackend(object):
    def __init__(self, topo: AwesomeLongFatTopo, debug=True) -> None:
        self.net = Mininet(topo)
        self.client, self.server = self.net.get('h1', 'n1')
        self.debug = debug

        self.net.start()
        self.server.cmd(
            f"iperf -s -e -i 1 > /tmp/awesome_LongFat_tcp_server.log &")

        self.send_tcp_package()
        CLI(self.net)
        self.clean()

    def send_tcp_package(self, t=10):
        self.client.cmd(
            f"iperf -c {self.server.IP()} -i 1 -b 900M,20M -e -t {t} > /tmp/awesome_LongFat_tcp_client.log &")

    def clean(self):
        if not self.debug:
            subprocess.run('sudo rm -rf /tmp/*.log', shell=True)

        self.net.stop()
        subprocess.run('sudo mn -c', shell=True)


if __name__ == '__main__':
    backwnd = BottleneckBackend(AwesomeBottleneckTopo())
    # backend = LongFatBackend(AwesomeLongFatTopo())
