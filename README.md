# BOM_generator
Author: Karthik kumaar

## Execution Steps:

**clone the repo inside the container**
```sh
sudo docker exec -it <contaiern id> bash 
git clone 
```
**Running the script**
```sh
python3 bom_script_new.py
```
**The output csv files are generated in the PWD**

**Copying the csv files from container to local** 
```sh	
#(Execute the below command in your local system)
sudo docker cp <container id>:<location of your csv files> <location of local host>
#example : sudo docker cp 4a6f50127d54:/opt/intel/openvino_2021.4.582/base_packages.txt /home	
```

