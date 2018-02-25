#This script pulls the IP addresses of devices from inventory.txt file
# and outputs a list of devices with the status of whether it is up or down.

import sys
import os
import subprocess
from threading import Thread

class Pinger(Thread):
    def __init__ (self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = False

    def __repr__(self):
        return "Pinger for '%s' status '%s'" % (self.ip, self.status)

    def run(self):
        with open(os.devnull, "wb") as limbo:
            result = subprocess.Popen(["ping", "-c", "2", "-q", self.ip],
                                      stdout=limbo, stderr=limbo).wait()
            if result:
                self.status = False
            else:
                self.status = True


hosts = []
with open('inventory.txt') as f:
    for line in f:
        host = Pinger(line.rstrip())
        hosts.append(host)
        host.start()


for host in hosts:
    host.join()
    if host.status:
        print "Host %s is up" % host.ip
        print "Entering %s to check free flash memory " % host.ip
        connection = netmiko.ConnectHandler(ip='%s', device_type='cisco_ios', username=username,
                                            password=password)

        check_interface = connection.send_command('sh run')

        print (check_interface)
    else:
        print "Host '%s' is down" % host.ip