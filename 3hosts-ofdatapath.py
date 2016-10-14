#!/usr/bin/python

"""
Three hosts called h1, h2, and h3 are connected as follows:

h1--------h2--------h3
we run the ofdatapath and ofprotocol on h2 to make an user space openflow switch on h2.

As mentioned in: https://github.com/mininet/openflow/blob/master/udatapath/ofdatapath.8.in

"ofdatapath is a userspace implementation of an OpenFlow
datapath.  It monitors one or more network device interfaces,
forwarding packets between them according to the entries in the flow table that it maintains. When it is used with ofprotocol, to connect the datapath to an OpenFlow controller, the combination is an OpenFlow switch."

In order to get some information such as port statisctics, flows ,etc on this switch we need to run the following commands on host h2: 

note: dp0 is the name we alloacted to the ofdatapath.

To show the ports use: 
dpctl show unix:/var/run/dp0 

To show the flows use: 
dpctl dump-flows unix:/var/run/dp0

After running ofdatapath and ofprotocol, we need to connect the openflow switch to the controller. So we need to run the POX controller on host h2 using:
./pox/pox.py forwarding.hub
 
Note!!! if the system have not found the controller for 30 sec., the default controller will work automatically.

After that we could ping host h1 via h3 or vica versa or we could have an iperf session between these two hosts. 
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology():
    "Create a network." 
    net = Mininet()

    print "*** Creating nodes"
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='192.168.10.1/24' )
    h2 = net.addHost( 'h2', mac='00:00:00:00:00:02')
    h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='192.168.10.3/24' )

    print "*** Creating controller"
    c4 = net.addController( 'c4', controller=RemoteController, ip='127.0.0.1', port=6633 )
    
    print "*** Creating links"    
    Link(h1, h2)
    Link(h2, h3)
    
    print "*** Starting network"    
    net.build()
    h2.cmd('ifconfig h2-eth0 0')
    h2.cmd('ifconfig h2-eth1 0')
    
    h2.cmd('sudo ofdatapath punix:/var/run/dp0 -d 004E46324304 -i h2-eth0,h2-eth1 -D')
    h2.cmd('sudo ofprotocol unix:/var/run/dp0 tcp:127.0.0.1:6633  --out-of-band &')

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

