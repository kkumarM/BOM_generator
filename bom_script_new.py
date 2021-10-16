#!/usr/bin/env python3
import subprocess
import csv
import argparse

# Run dpkg license script generator
subprocess.call("./dpkg-licenses/dpkg-licenses", shell = True)
print("Generating Dpkg Licenses csv file")

# Generate dpkg packages (csv)
with open('base_image.csv', 'w', newline='') as f:
	headers = ['Name','Origin','Licenses']
	writer = csv.DictWriter(f, fieldnames=headers)
	writer.writeheader()
	with open("out.csv", 'r') as csv_read:
		for row in csv.DictReader(csv_read):
			#print(row)
			name = (row["Name"])
			origin = subprocess.check_output("apt-cache show {} | awk '/^Homepage/'".format(name), shell = True).decode().split()
			print("name:", row["Name"])
			print("origin:", origin)
			if len(origin) !=0 :
				row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': origin[1], 'Licenses': row['Licenses']}
			else:
				row = {'Name': str(row['Name'])+"=="+str(row['Version']), 'Origin': "", 'Licenses': row['Licenses']}
			# Now write a sample row:
			
			writer.writerow(row)  # Automatically skips missing keys
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
		
