#!/usr/bin/env python3
# Author: Karthik Kumaar 
import subprocess
import csv
import os 
import argparse
import threading

# Get docker base image packages from user 
parser = argparse.ArgumentParser(description='Enter your base image packages text file.')
parser.add_argument('base_image', type=str, 
                    help='base_packages.txt')
args = parser.parse_args()
base_packages_list = []
GPL_package_list = []

try:
	with open('base_image_packages/{}.txt'.format(args.base_image)) as f:
	    base_packages_list = f.read().splitlines()
except:
	print("Base Image package file not found")

# Create Folders
out_path = os.getcwd() + "/output"
print(out_path)
sources_path = os.path.join(out_path,'GPL_license_source_codes')
output_csv_path = os.path.join(out_path, 'CSV_outputs')
if not os.path.exists(out_path):
	path = os.makedirs(out_path)
if not os.path.exists(sources_path):
    path = os.makedirs(sources_path)
if not os.path.exists(output_csv_path):
    path = os.makedirs(output_csv_path)

# Run Autoremove to remove automatically installed packages
subprocess.run("apt autoremove", shell = True)

# Run dpkg license script generator
subprocess.run("./dpkg_license_gen/dpkg-licenses.sh", shell = True)
print("Generating Dpkg Licenses csv file")

# Generate dpkg packages (csv)
print("Generating Origin for dpkg installed packages ............")
with open('output/CSV_outputs/installed_packages.csv', 'w', newline='') as f:
	headers = ['Name','Origin','Licenses']
	writer = csv.DictWriter(f, fieldnames=headers)
	writer.writeheader()
	with open("out.csv", 'r') as csv_read:
		for row in csv.DictReader(csv_read):
			Name = row["Name"].split(":")
			if Name[0] not in base_packages_list:
				if row["Licenses"].startswith("GPL") or row["Licenses"].startswith("LGPL"):
					GPL_package_list.append(row["Name"])
				origin = subprocess.check_output("apt-cache show {} | awk '/^Homepage/'".format(row["Name"]), shell = True).decode().split()
				if len(origin) !=0 and row["Name"] not in base_packages_list:
					row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': origin[1], 'Licenses': row['Licenses']}
				else:
					row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': "ubuntu", 'Licenses': row['Licenses']}
				# Now write the rows:				
				writer.writerow(row)  # Automatically skips missing keys

print("Generating sources for GPL and LGPL dpkg packages ............")
subprocess.run("cp /etc/apt/sources.list /etc/apt/sources.list~", shell = True)
subprocess.run("sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list", shell = True)
subprocess.run("apt-get update", shell = True)
for i in GPL_package_list:	
	name = i.split(":")
	try:
		subprocess.run("apt-get source {} ".format(name[0]), cwd='output/GPL_license_source_codes',shell = True)
	except Exception as e:
		output = str(e.output)
		print(output)
				
'''
# Check GPL and LGPL licenses

with open('CSV_outputs/installed_packages.csv') as csv_read:
	for row in csv.DictReader(csv_read):
		if row["Licenses"].startswith("GPL") or row["Licenses"].startswith("LGPL"):
			package_name = row["Name"].split("==")
			print("GPL Package Name:", package_name)
			subprocess.call("cp /etc/apt/sources.list /etc/apt/sources.list~", shell = True)
			subprocess.call("sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list", shell = True)
			subprocess.call("apt-get update", shell = True)
			subprocess.check_output("apt-get source {} ".format(package_name[0]), cwd='GPL_license_source_codes',shell = True).decode().split()
		else:
			continue


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
		
