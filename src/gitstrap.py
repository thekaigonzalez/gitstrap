#!/usr/bin/python3
import argparse
import os
import tarfile
import requests
import json
import sys

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='install Command')

parser_install = subparsers.add_parser("install", help="Installer.")
parser_install.add_argument("package", type=str, help="package to install")
parser.add_argument("-v", "--verbose", default="store_true", help="Print information about the installations.");

args = parser.parse_args()
def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename
try:
	print("installing " + args.package + "...")
	if requests.get("https://github.com/thekaigonzalez/" + args.package).status_code == 404:
		print("target " + args.package + " not found!")
	else:
		print("found repository. Downloading information..")
		#https://api.github.com/repos/twbs/bootstrap. (DOC)
		repo = requests.get("https://api.github.com/repos/thekaigonzalez/" + args.package)
		repo_info = repo.json()
		print("Name: " + repo_info["name"])
		print("Main Language: " + repo_info["language"])
		print("would you like to install this repository?")
		ins = input("[Y/n] ")
		if ins.lower() == "y":
			print("downloading source code...")
			#https://api.github.com/repos/User/repo/tarball/master
			print("checking repository https://thekaigonzalez.github.io/cdn/ for " + args.package)
			req = requests.get("https://thekaigonzalez.github.io/cdn/" + args.package + ".tar.gz")
			if (req.status_code == 404):
				print("Resource was found on GIT but not the server!")
			else:
				download_file("https://thekaigonzalez.github.io/cdn/" + args.package + ".tar.gz")
				print("source code installed. extracting...")
				my_tar = tarfile.open(args.package + '.tar.gz')
				my_tar.extractall("./") # specify which folder to extract to
				my_tar.close()
				print("entering" + args.package)
				print("running 'make & sudo make install'")
				os.system("make -C " + args.package)
				if os.system("sudo make -C " + args.package + " install") == -1:
					print("Make install failed!")
				else:
					print("installed!")
		else:
			quit()
except AttributeError or NamespaceError as e:
	print("Did you specify an operation?\nError: " + str(e))
except ConnectionError:
	print("I do not have connection. Please make sure you are connected to the internet")