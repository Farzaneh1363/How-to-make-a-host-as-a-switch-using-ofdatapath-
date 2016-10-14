# How-to-make-a-host-as-a-switch-using-ofdatapath-
We have a topology of 3 host and wants to show how to make the second host to act as a openflow switch using ofdatapath and of protocol. 

After you run the code in : https://github.com/Farzaneh1363/How-to-make-a-host-as-a-switch-using-ofdatapath-/blob/master/3hosts-ofdatapath.py

Then you need to open an xterm on host h2 via mininet console as follows: 
    mininet> xterm h2 

And in h2 run your controller. In this example we run POX controller in h2: 

    ./pox/pox.py forwarding.hub
    
After that you can run an iperf session between these two hosts and compare the result with the kernel mode switches.
you could see the userspace switch is much slower than OVS in kernel space. 
    


