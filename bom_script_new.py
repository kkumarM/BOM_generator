#!/usr/bin/env python3

# Copyright (c) 2020 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#
# Author: Karthik Kumaar <karthikx.kumaar@intel.com>
import subprocess
import csv
import os 
import argparse

# Get docker base image packages from user 
parser = argparse.ArgumentParser(description='Enter your base image packages text file.')
parser.add_argument('base_image', type=str, 
                    help='base_packages.txt')
args = parser.parse_args()
base_packages_list = []
try:
	with open('base_image_packages/{}.txt'.format(args.base_image)) as f:
	    base_packages_list = f.read().splitlines()
except:
	print("Base Image package file not found")

# Create Folders
work_path = os.getcwd()
print(work_path)
sources_path = os.path.join(work_path,'GPL_license_source_codes')
output_csv_path = os.path.join(work_path, 'CSV_outputs')
if not os.path.exists(sources_path):
    path = os.makedirs(sources_path)
if not os.path.exists(output_csv_path):
    path = os.makedirs(output_csv_path)

# Run dpkg license script generator
subprocess.call("./dpkg-licenses/dpkg-licenses.sh", shell = True)
print("Generating Dpkg Licenses csv file")

# Generate dpkg packages (csv)
print("Generating Origin for dpkg installed packages ............")
with open('CSV_ouputs/installed_packages.csv', 'w', newline='') as f:
	headers = ['Name','Origin','Licenses']
	writer = csv.DictWriter(f, fieldnames=headers)
	writer.writeheader()
	with open("out.csv", 'r') as csv_read:
		for row in csv.DictReader(csv_read):
			if row["Name"] not in base_packages_list:
				origin = subprocess.check_output("apt-cache show {} | awk '/^Homepage/'".format(row["Name"]), shell = True).decode().split()
				if len(origin) !=0 and row["Name"] not in base_packages_list:
					row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': origin[1], 'Licenses': row['Licenses']}
				else:
					row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': "", 'Licenses': row['Licenses']}
				# Now write the rows:				
				writer.writerow(row)  # Automatically skips missing keys

# Check GPL and LGPL licenses
print("Generating sources for GPL and LGPL dpkg packages ............")
with open('CSV_ouputs/installed_packages.csv') as csv_read:
	for row in csv.DictReader(csv_read):
		if row["Licenses"].startswith("GPL") or row["Licenses"].startswith("LGPL"):
			package_name = row["Name"]
			subprocess.call("cp /etc/apt/sources.list /etc/apt/sources.list~", shell = True)
			subprocess.call("sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list", shell = True)
			subprocess.call("ap-get update", shell = True)
			subprocess.check_output("apt-get source {} ".format(package_name[0]), cwd='GPL_license_source_codes',shell = True).decode().split()
		else:
			continue

'''
# Generate pip freeze packages (csv)

package_name = subprocess.check_output("pip3 freeze --all", shell = True).decode().split()
with open("dpkg-licenses/pip-freeze-packages.csv", 'w', newline='') as f:
	headers = ['Name','Origin','Licenses']
	writer = csv.DictWriter(f, fieldnames=headers)
	writer.writeheader()	
for pkg in package_name:
	pkg_name = pkg.split("==")
	pip_origin = subprocess.check_output("pip3 show {} | awk '/^Homepage/'".format(pkg_name[0]), shell = True).decode().split()
	pip_license = subprocess.check_output("pip3 show {} | awk '/^License/'".format(pkg_name[0]), shell = True).decode().split()
	print(pip_license)
	if len(pip_origin) !=0 :
		row = {'Name': pkg, 'Origin': pip_origin[1], 'Licenses': pip_license[1]}
		print(row)					
	else:
		row = {'Name': pkg, 'Origin': "", 'Licenses': pip_license[1]}
'''	
		