import docker
from io import StringIO
import tarfile

client = docker.from_env()
# name = "openvino/ubuntu18_runtime:2021.2"
# tmp_cont=client.containers.run('hello-world')
# print(tmp_cont)
# cmd = "/bin/sh -c 'echo hello_world'"
# _out = tmp_cont.exec_run(cmd,stream=True,demux=False)
# #_out = name.exec_run("dpkg-query -W -f='${package}\n' > openvino/ubuntu18_runtime:2021.2.txt")
# print(_out.output)
#"dpkg-query -W -f='${package}\n' > openvino/ubuntu18_runtime:2021.2.txt"
#client.get_archive(tmp_cont, '/')
#container.exec_run()

#container = client.containers.run('openvino/ubuntu18_runtime:2021.2', detach=True)
container = client.containers.list()
container_ID = [container.short_id for container in container]
print(container[6])
#print(container_ID)

for i in container:
	if container_ID[0] == i.short_id:
		#print (i)
		pass

cmd = "/bin/bash -c 'apt-get update && apt-get install git'"
cmd1 = "/bin/bash -c 'cd /app' && git clone https://github.com/kkumarM/BOM_generator.git"
cmd2 = "python3 bom_script_new.py"
_,out = container[6].exec_run(cmd1,stream=True,demux=False)
#res,stat = container[6].get_archive('config.json', chunk_size=2097152, encode_stream=False)

for data in out:
	print(data.decode("utf-8"))
# for d in res:
# 	print(d)
# 	pw_tar = tarfile.TarFile(fileobj=StringIO(d.decode('utf-8')))
# 	pw_tar.extractall("./")
# print(res)