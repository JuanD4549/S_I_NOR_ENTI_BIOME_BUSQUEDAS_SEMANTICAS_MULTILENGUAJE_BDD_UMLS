import docker
import os
from pathlib import Path
from subprocess import call
################################################################
#------------Inicia el contenedor de docker METAMAP------------#
client = docker.from_env()
contenedor=client.containers.run("metamap", auto_remove=True, detach=True, ports={"80/tcp":80})
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
os.system('docker compose up')
if os.stat('.\output.txt').st_size == 0:
    print("NO esta el documento outout")
    exit()
print("si esta el documento outout")
################################################################
#--------------------Inicia de alignment-----------------------#
os.system('python alignment.py')
if(os.stat(".\objects.txt")):
        print("NO esta el documento objects")
        exit()
print("si esta el documento objects")
#contenedor.stop()