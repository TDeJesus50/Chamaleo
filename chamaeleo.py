#!/usr/bin/env python


"""
Tool: File Retriever via VyprVPN
Author: Terrance DeJesus
Version: 1.0
"""

import urllib, os, datetime, argparse, hashlib, gzip, shutil
from termcolor import colored
from netifaces import interfaces, ifaddresses, AF_INET

parser = argparse.ArgumentParser(description='Chamaeleo is a tool used to quickly pull down binaries from remote servers via VyperVPN, using the fastest configuration available. The filenames will be the MD5 hash of the file itself and then the file will be gzipped. Please note, a VyperVPN account is necessary')
parser.add_argument('-u', '--username', help="VyperVPN Username")
parser.add_argument('-p', '--password', help="VyperVPN Password")
parser.add_argument('-r', '--resource', help="URL or Destination of Binary")
parser.add_argument('-f', '--file', help="Pull from Multiple URLs Inside a Specific File")
args = parser.parse_args()
username = args.username
password = args.password
url = args.resource
mfile = args.file



def introduction():
	print colored("""

 _____   __   __     ___      _      _     ___      ______   _       ______   ______
|  ___| |  |_|  |   / _ \    | \    / |   / _ \    | _____| | |     | _____| |  __  |
| |     |       |  / |_| \   |  \  /  |  / |_| \   | __|    | |     | __|    | |  | |
| |___  |   _   | /   _   \  |   \/   | /   _   \  | |_____ | |____ | |____  | |__| |
|_____| |__| |__|/___| |___\ |__|\/|__|/___| |___\ |______| |______||______| |______|

	
   --------/
   \       --------/_
----\        ----    \___
            (__0_)       \_
    \                      \               _______
     \         ___----------              | ___   |
               \/ ________________________|____|  |
                \/________-__ ____________________|
      __\                   /              
     /    ------------------
    /
__ /


Welcome to Chamaeleo, a tool used to retrieve binaries through VyperVPN. Please note, you must have an active VyperVPN account in order to use this tool. 
""", 'green')
	
	cont =  raw_input("Please press '{}' to continue..\n".format(colored('ENTER', 'yellow')))
	

def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()
	f.close()



def vpnsetup():
	print "{} Setting up VPN connection....{}".format(colored(datetime.datetime.now(), 'yellow'), colored('[OK]', 'green'))
	
	os.system('vyprvpn login {} {}'.format(username, password)) 
	os.system('vyprvpn connect')


def vpndisconnect():
	os.system('vyprvpn logout')
	os.system('vyprvpn disconnect')
	os.system('dhclient -r')
	os.system('dhclient')

def retrieval():
	if mfile:
		print "{} Retrieving Files....{}".format(colored(datetime.datetime.now(), 'yellow'), colored('[OK]', 'green'))
		with open(mfile, 'rb') as f:
			urllist = f.readlines(); urllist = [url.strip() for url in urllist]
		for url in urllist:
			print "{} Calculating File MD5 Hash for file from {}....{}".format(colored(datetime.datetime.now(), 'yellow'), url, colored('[OK]', 'green'))
			urllib.urlretrieve(url, 'newfile')
			filehash = md5('newfile')
			
			print "{} Compressing file and renaming as {}.gzip....{}".format(colored(datetime.datetime.now(), 'yellow'), colored(filehash, 'red'), colored('[OK]', 'green'))
			with open('newfile', "rb") as f_in, gzip.open('/home/{}.gz'.format(filehash), 'wb') as f_out:
				f_out.writelines(f_in)
				
			f_in.close(); f_out.close
			os.remove('newfile')
		
	else:	
		print "{} Retrieving File....{}".format(colored(datetime.datetime.now(), 'yellow'), colored('[OK]', 'green'))
		urllib.urlretrieve(url, 'newfile')
	
		print "{} Calculating File MD5 Hash....{}".format(colored(datetime.datetime.now(), 'yellow'), colored('[OK]', 'green'))
		filehash = md5('newfile')

		print "{} Compressing file and renaming as {}.gz....{}".format(colored(datetime.datetime.now(), 'yellow'), colored(filehash, 'red'), colored('[OK]', 'green'))
		with open('newfile', "rb") as f_in, gzip.open('/home/{}.gz'.format(filehash), 'wb') as f_out:
			f_out.writelines(f_in)
		f_in.close(); f_out.close
		os.remove('newfile')
	

if __name__ == "__main__":
	os.system('clear')
	introduction()
	vpnsetup()
	retrieval() 
	vpndisconnect()
	print "{} Done....{}".format(colored(datetime.datetime.now(), 'yellow'), colored('[OK]', 'green'))


	
