#!/usr/bin/env python
# Setup for web-map
import time
try:
	i = 5
	print "WARNING, FOR RUNNING CORRECTLY \"setup.py\" YOU NEED TO HAVE ALREADY INSTALLED \"pip\""
	print "for installing it type: \"sudo apt-get install pip\" on the terminal"
	print "press CONTROL+C for aborting"
	while i > 0:
		print i
		i-=1
		time.sleep(1)
except KeyboardInterrupt:
	exit(0)
print "[*] Starting with the installation..."
time.sleep(1)
try:
	import os
	print "[+] \"os\" already installed"
except:
	print "[!] \"os\" is not installed and setup.py cannot install it,\nplease install it manually by typing: \"sudo pip install os\" on the terminal"
	exit(0)	
try:
	import sys
	print "[+] \"sys\" already installed"
except:
	print "[+] \"sys\" is not installed, installing..."
	os.system("sudo pip install sys")
try:
	import requests
	print"[+] \"requests\" already installed"
except:
	print "[+] \"requests\" is not installed, installing..."
	os.system("sudo pip install requests")
default_uris = ".htaccess\nlogs\nlogs.txt\nadmin\nadmin.php\nwp-admin\nrobots.txt\nmod\nmod.php\nwp-content\nwp-admin\nlogin\nlogin.php\nindex.php\nindex\nindex.html"
print "\n[?] web-map folder is going to be installed on /bin/web-map"
chng = raw_input("Do you want to change this directory? Y/n ")
if chng == 'y' or chng == 'Y':
	new_directory = raw_input("Type the new path to the folder: ")
	os.system("sudo mkdir "+new_directory)
	os.system("echo \"\" > "+new_directory+"/logs.txt")
	os.system("echo \"\" > "+new_directory+"/default_uris.txt")
else:
	os.system("sudo mkdir /bin/web-map")
	os.system("echo \"\" > /bin/web-map/logs.txt")
	os.system("echo \"%s\" > /bin/web-map/default_uris.txt" % default_uris)

print "[+] Installation completed correctly"
