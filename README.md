# BOM_generator
Author: Karthik Kumaar 

## Pre-requisites
```
$ pip3 install docker termcolor
```

## Execution Steps:
```sh
$ sudo python3 run.py
# Follow the terminal instructions
```

**Output Structure**
```sh
#CSV_outputs:
    - pip3_freeze_all_packages.csv -> Contains pip packages installed along with License and Origin in the contianer
    - pip3_freeze_all_packages.txt -> Containes pip package names with version
    - installed_packages.csv -> Contains user installed dpkg packages excluding base packages.
```

**Generating Base Package text file - Externally**
```sh
sudo docker run -it -u0 openvino/ubuntu18_runtime:2021.4 
dpkg-query -W -f='${package}\n' > openvino_ubuntu18_runtime_2021_4.txt
```
