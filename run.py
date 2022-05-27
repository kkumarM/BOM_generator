#!/usr/bin/env python3
# Author: Karthik Kumaar


import docker
import subprocess
import os
import sys
from termcolor import colored
from io import StringIO,BytesIO
import tarfile

class GenerateBOM(object):
	def __init__(self):
		self.client = docker.from_env()
		self.obj_id = ""

	def get_running_containers(self):
		"""
		Function to fetch the running containers in the host machine
		Parameters : None
		Return: List
		"""
		
		running_containers = self.client.containers.list()
		container_ID = [container.short_id for container in running_containers]
		container_name = [container.name for container in running_containers]
		return container_name, container_ID, running_containers 

	def create_base_package(self, image, name):
		"""
		Function to create base package used in docker images
		Parameters : base image, text file name
		Return: generated package file
		"""
		cmd = "dpkg-query -W -f='${package}\n'"
		temp_cont = self.client.containers.run(image=image, command = cmd)
		with open("BOM_main/base_image_packages/" + name + ".txt","w") as file:
			file.write(temp_cont.decode("utf-8"))
		return name
		

	def run_bom_generator(self, base_package, cont_id):
		pwd = os.getcwd()
		print("cont id:", self.obj_id)
		#cmd = "/bin/bash -c 'whoami && apt-get update && apt-get install git'"
		cmd1 = f"sudo docker cp {pwd}/BOM_main  {cont_id}:/"
		#cmd2 = "/bin/bash -c 'git clone https://github.com/kkumarM/BOM_generator.git'"
		cmd3 = f"/bin/bash -c 'cd /BOM_main && python3 bom_script_new.py {base_package}.txt'"
		print(self.obj_id)
		subprocess.run(cmd1, shell=True)
		#_,out = self.obj_id.exec_run(cmd1,stream=True,demux=False,detach=False,user="root")
		#_,out1 = self.obj_id.exec_run(cmd1,stream=True,demux=False,detach=False,user="root")
		_,out2 = self.obj_id.exec_run(cmd3,stream=True,demux=False,detach=False,user="root")		
		# for data in out:
		# 	print(data.decode("utf-8"))
		for data in out2:
			print(data.decode("utf-8"))
		# for data in out3:
		# 	print(data.decode("utf-8"))
		res,stat = self.obj_id.get_archive('BOM_main/output', chunk_size=2097152, encode_stream=False)
		# Save Output files from container to local
		filetype = BytesIO(b"".join(b for b in res))
		tar = tarfile.open(fileobj=filetype)
		tar.extractall("./")
		return ("Files Saved in current Directory")


	def get_user_inputs(self):
		"""
		function to get inputs from user to get the base package, 
		if doesn't exists, genereate one
		Parameters : None
		Return: None
		"""
		container_name, container_id, running_containers = self.get_running_containers()
		print('\n',colored("List of Running Containers:", "green"),'\n')
		for i,j in zip(container_id,container_name):
			print(i,":",j)

		try:
			input_container_id = input(colored("Enter Container ID:","yellow"))
			if input_container_id in container_id:
				pass
			else:
				print(colored("Container ID doesn't exists, Please verify !", "red"))
				input_container_id = input(colored("Enter Container ID:","yellow"))
			for obj in running_containers:
				if input_container_id == "":
					print(colored("Container ID is not Valid, Exiting ...", "red"))
					sys.exit(0)
				if input_container_id == obj.short_id:
					self.obj_id = obj
			image = input(colored("Enter Base Package (eg: openvino/ubuntu18_runtime:2021.2):","yellow"))
			base_package = image.replace('.','_').replace(':','_').replace('/','_')
			if os.path.exists(f"BOM_main/base_image_packages/{base_package}.txt"):
				print("Inside")
				print(colored("Base package already present !","cyan"))	
				self.run_bom_generator(base_package,input_container_id)

			else:
				print(colored("Base package not present !","cyan"))	
				out = input(colored("Do you want to create one (yes/no):","cyan"))
				if out == "yes" or out == "y":
					print(base_package)
					file_name = self.create_base_package(image, base_package)
					self.run_bom_generator(base_package,input_container_id)
				else:
					print(colored("Exiting....","red"))
				# if out == "yes":
				# 	self.create_base_package()			
			
		except Exception as e:
			print(e.__class_)
		


obj = GenerateBOM()
obj.get_user_inputs()


