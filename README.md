# pySNMP-tests
Scripts to demostrate pySNMP functionality with network devices

#Libraries needed
You are going to need pySNMP http://pysnmp.sourceforge.net/

#MPLS
This script displays information of all the LSPs in a device in an ordered table. You may see source, destination, path(s) ERO and RRO. If you only need to quickly check where all the different LSPs traffic is flowing this can help a lot.

#IPSec
Basically the same idea of the MPLS script for IPSec, as it shares the same base code, so this script can be used as an example for other device protocols, you just have to get the proper OIDs and that's about it.
