import os
import sys
from netaddr import IPNetwork

f1 = open('subnet.txt','r')




devices = f1.readlines()

for device in devices:
    column = device.split()
    #print column[0]+ "Network expsnd "
    for ip in IPNetwork(column[0]):
    	print ip
 
f1.close()









 
