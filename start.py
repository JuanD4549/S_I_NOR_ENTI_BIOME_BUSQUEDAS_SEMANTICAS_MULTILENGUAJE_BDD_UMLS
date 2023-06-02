import docker
import os
from pathlib import Path

client = docker.from_env()

contenedor=client.containers.run("metamap", auto_remove=True, detach=True, ports={"80/tcp":80})
os.system('python translateFromFiles.py')
fileName = r".\ingles.txt"
fileObj = Path(fileName)
if(fileObj.is_file()):
    os.system('python alignment.py')
    contenedor.stop()
