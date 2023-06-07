import docker
import os
from pathlib import Path
from subprocess import call
################################################################
#------------Inicia el contenedor de docker METAMAP------------#
client = docker.from_env()
#contenedor=client.containers.run("metamap", auto_remove=True, detach=True, ports={"80/tcp":80})
################################################################
#--------------------Ingreso de la consulta--------------------#
with open("spanish.txt","w", encoding='utf-8') as txtSpanish:
      texto=input("Ingresa tu consulta: \n")
      txtSpanish.write(texto)
################################################################
#--------------Inicia el proceso de Traducción-----------------#
os.system('python translateFromFiles.py')
#call(["python", "translateFromFiles.py"])
if os.stat('.\ingles.txt').st_size == 0:
    print("NO esta el documento traducido")
    exit()
print("si esta el documento traducido")
################################################################
#--------------------Inicia de awesomeAlignment----------------#

################################################################
#--------------------Inicia de alignment-----------------------#
#os.system('python alignment.py')
filePath = r".\output.txt"
filePath2= r".\objects.txt"
fileAlignment = Path(filePath)
fileAlignment2 = Path(filePath2)
if(not (fileAlignment.is_file() and fileAlignment2.is_file()) ):
        print("NO esta el documento ALignment")
        exit()
print("si esta el documento Aligment")
#contenedor.stop()