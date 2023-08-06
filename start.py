import os
from time import sleep
import app.static.python.translateFromFiles as translateFromFiles
import app.static.python.alignment as alignment
import requests
import app.static.python.similarity as similarity

################################################################
#------------Inicia el contenedor de docker METAMAP------------#
os.system("docker start practical_murdock")
os.system("docker start awesomeaigment-similarity-1")
################################################################
#--------------------Ingreso de la consulta--------------------#
spanishText=[]
inputs=input("Ingresa tu consulta: \n")
spanishText.append(inputs)
while True:
    inputs = input("Tiene otra consulta: (si no tiene presione enter) \n")
    if inputs:
        spanishText.append(inputs)
    else:
        break
#print(spanishText)
################################################################
#--------------Inicia el proceso de Traducción-----------------#
print("Se esta traduciendo al ingles")
englishText=translateFromFiles.translate(spanishText)
################################################################
#--------------------Inicia de awesomeAlignment----------------#
print("Se esta ejecutando el awesomeAlignment")
r=requests.get('http://localhost:3000/awesomeAigment')
print(r.status_code)
################################################################
#--------------------Inicia de alignment-----------------------#
print("Se esta ejecutando el etiquetado")
if r.status_code!=200:
    exit()
objects=alignment.getEntitiesAllClefSpanish(englishText,spanishText)
################################################################
#--------------------Inicia de la busquedea del atomo-----------------------#
print("Inicia la busqueda del atomo")
similarity.validar(objects)