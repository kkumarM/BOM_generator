#!/usr/bin/env python3
# Author: Karthik Kumaar


import docker
import subprocess
import os
from termcolor import colored

class GenerateBOM(object):
	def __init__(self):
		self.client = docker.from_env()

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

	def create_base_package(self):
		"""
		Function to create base package used in docker images
		Parameters : None
		Return: 
		"""
		new_base_package = input(colored("Enter base image package used in the docker image:","gray"))
		name = new_base_package.replace('.','_').replace(':','_').replace('/','_')
		temp_cont = self.client.create_container(image=new_base_package,command = "dpkg-query -W -f='${package}\n' > {0}}.txt".format(name))
		container.exec_run()

	def get_user_inputs(self):
		"""
		function to get inputs from user to get the base package, 
		if doesn't exists, genereate one
		Parameters : None
		Return: 
		"""
		global obj_id
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

			for obj in running_containers:
				if input_container_id == obj.short_id:
					obj_id = obj
			base_package = input(colored("Enter Base Package (eg: openvino/ubuntu18_runtime:2021.2):","yellow"))
			base_package = base_package.replace('.','_').replace(':','_').replace('/','_')
			if os.path.exists(f"base_image_packages/{base_package}.txt"):
				print("Inside")
				print(colored("Base package already present !","cyan"))	
				cmd = 'python3 bom_script_new.py'
				print(obj_id)
				out = obj_id.exec_run('/bin/sh -c ls',stream=True, demux=False)
				# print(stderr)
				# print(stdout)
				print(out.output)
			else:
				print(colored("Base package not present !","cyan"))	
				out = input(colored("Do you want to create one (yes/no):","cyan"))
				# if out == "yes":
				# 	self.create_base_package()
				
			
		except Exception as e:
			print(e.__class_)
		


obj = GenerateBOM()
obj.get_user_inputs()


