# BOM_generator
Author: Karthik Kumaar 

## Execution Steps:

**clone the repo inside the container**
```sh
sudo docker exec -it <contaiern id> bash 
git clone https://github.com/kkumarM/BOM_generator.git
```
**Running the script**
```sh
python3 bom_script_new.py openvino_ubuntu18_runtime_2021_2
```
#### Note: 
The argumet needs to be in the same format as mentioned above. For Ex: if you base image is openvino/ubuntu18_runtime:2021.2

**The output csv files are generated in CSV_outputs folder**

**Copying the csv files from container to local** 
```sh	
#(Execute the below command in your local system)
sudo docker cp <container id>:<location of your csv files> <location of local host>
#example : sudo docker cp 4a6f50127d54:/opt/intel/openvino_2021.4.582/base_packages.txt /home	
```
**Output Structure**
```sh
#CSV_outputs:
    - pip3_freeze_all_packages.csv -> Contains pip packages installed along with License and Origin in the contianer
    - pip3_freeze_all_packages.txt -> Containes pip package names with version
    - installed_packages.csv -> Contains user installed dpkg packages excluding base packages.

#GPL_license_source_codes:
 - This folder contains the source codes for GPL and LGPL license packages use in the docker container
```


**Generating Base Package text file**
```sh
sudo docker run -it -u0 openvino/ubuntu18_runtime:2021.4 
dpkg-query -W -f='${package}\n' > openvino_ubuntu18_runtime_2021_4.txt
```
