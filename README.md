# SISTEMA INFORMÁTICO PARA LA NORMALIZACIÓN DE ENTIDADES BIOMÉDICAS BASADOS EN BÚSQUEDAS SEMÁNTICAS MULTILENGUAJE, SOBRE LA BASE DE DATOS MÉDICOS UMLS.

## Requisitos necesarios
1. Contenedores de docker instalados:
    * UMLS
    * AwesomeAigment
    * Metamap
2. La version de python utiliza para ejecutar el sistema debe ser 3.8.8+ dentro de un entorno virtual de python
3. Instalar las librerias necesarias, dirigir la ruta la carpea **app** y ejecutar el siguiente comando
    `pip install -r requirements.txt`
### Instalar el contenedor AwesomeAigment
    Ejecutar el siguiete comando desde la raiz principal del proyecto
`docker compose -p awesomeaigment up`
## Ejecutar el proyecto
1. Establecer la raiz del pryecto en la carpeta **app** y ejecutar el siguiente comando
    `python app.py`
