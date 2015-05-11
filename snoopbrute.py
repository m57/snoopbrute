#!/usr/bin/env python
#
# m57 / @_x90__
#
##########################

import os
import sys
import re
import time
import commands
from threading import Thread

hosts = []
threads = []
num_threads = 5
target_dns = ""
VERSION = "1.0"

def help():
	print "Usage: %s [target_DNS] [wordlist (Optional, default: domain_wordlist.txt)] [threads (Optional, default: 3)] " % sys.argv[0]
	sys.exit()

def valid_ip(ip):
	if re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$").match(ip):
                return True
        elif "." in ip:
                return True
	else:
		return False

def banner():

	print '   ___    _  _     ___     ___      ___    ___     ___     ___     ___    _____  '
	print '  / __|  | \| |   / _ \   / _ \    | _ \  | _ )   | _ \   / _ \   / _ \  |_   _| '
	print '  \__ \  | .` |  | (_) | | (_) |   |  _/  | _ \   |   /  | (_) | | (_) |   | |   '
	print '  |___/  |_|\_|   \___/   \___/   _|_|_   |___/   |_|_\   \___/   \___/   _|_|_  '
	print '_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| '
	print '`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\'"`-0-0-\' '
	print "_________________________________________________________________________________"
	print "\t\t\t\t\t\t\t\tv. %s @_x90__" % VERSION

def dns_cache_lookup(host, target_ns, x):

	resolved = []
	cmd = "dig +short +norecurse %s @%s" % (host.strip(), target_ns.strip())
#	print "thread: %d -> %s" % (x, cmd)
	out = commands.getstatusoutput(cmd)[1]
#	print out
	if "\n" in out:
		for i in out.split("\n"):
			resolved.append(i.strip())

		for i2 in resolved:
			if (valid_ip(i2.strip())):
				print "[Thread id: %d] Host identified: %s:%s" % (x, host[:-1], i2) 

	else:
		if (valid_ip(out)):
			print "[Thread id: %d] Host identified: %s:%s" % (x, host[:-1], out)

	return

def parse_host_file(file):

	print "Buffering input host file: %s" % file

	with open(file, "r") as f:
		for i in f:
			try:
				if len(i) > 1 :
					hosts.append(i)
			except:
				print "Failed trying to parse host file"
	f.close()

class sender(Thread):

        def __init__(self, threadnum, data_package):
                Thread.__init__(self)
                self.data = data_package
                self.tnum = threadnum
                self.host_to_query = data_package[0]
		self.target_ns	= data_package[1]

        def run(self):
		dns_cache_lookup(self.host_to_query, self.target_ns, self.tnum)

def start_cache_snoop():

	threads = []
	for i in hosts:
		threads.append(sender(hosts.index(i), [i, target_dns]))

	count = 0
	for i in range(0, len(threads)):
		threads[i].start()
		count += 1


if __name__ == "__main__":

	path = os.getcwd() + "/"

	if (len(sys.argv) == 2):
		target_dns = sys.argv[1]
		if (os.path.isfile(path + "domain_wordlist.txt")):
			parse_host_file("domain_wordlist.txt")
		else:
			help()
			print "[!] Cannot find ./domain_wordlist.txt, either git clone https://github.com/m57/snoopbrute again or supply a wordlist!\n"

	elif (len(sys.argv) == 3):
		target_dns = sys.argv[1]
		if (os.path.isfile(path + sys.argv[2])):
			parse_host_file(sys.argv[2])
		else:
			help()
			print "[!] Cannot find ./domain_wordlist.txt, either git clone https://github.com/m57/snoopbrute again or supply a wordlist!\n"
	else:
		help()

	banner()

	print "Starting..."


	print "Executing non-recursive queries with %d threads\nTarget >>> %s\n" % (num_threads, target_dns)
	start_cache_snoop()
