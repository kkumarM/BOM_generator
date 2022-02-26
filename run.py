#!/usr/bin/env python3
# Author: Karthik Kumaar


import docker
import subprocess
import os
from termcolor import colored

class GenerateBOM(object):
	def __init__(self):
		pass

	def get_running_containers(self):
		client = docker.from_env()
		running_containers = client.containers.list()
		container_ID = [container.short_id for container in running_containers]
		container_name = [container.name for container in running_containers]
		return container_name

	def get_user_inputs(self):
		container_name = self.get_running_containers()
		print('\n',colored("List of Running Containers:", "green"),'\n')
		for i,j in enumerate(container_name):
			print(f"{i+1}:",j)
		try:
			input_container = input(colored("Enter Container Name:","yellow"))
			if input_container in container_name:
				base_package = input(colored("Enter Base Package (eg: openvino/ubuntu18_runtime:2021.2):","yellow"))
				base_package = base_package.replace('.','_').replace(':','_').replace('/','_')
				if os.path.exists(f"base_image_packages/{base_package}.txt"):
					print("Inside")
					print(colored("Base package already present !","cyan"))	
				else:
					print(colored("Base package not present !","cyan"))	
					out = input(colored("Do you want to create one (yes/no):","cyan"))
					print(out)			
			else:
				print(colored("Container name doesn't exists, Please verify !", "red"))
			
		except Exception as e:
			print(e.__class_)
		


obj = GenerateBOM()
obj.get_user_inputs()


