from static.python.traductor import translate
from static.python.etiquetado import getEntitiesAllClefSpanish
from static.python.similitud import validar
from flask import Flask,render_template,request
import re
import requests

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    #return "<p>Ingreso de consulta:</p>"
    print(request.form)
    data={}
    if request.method == 'POST':
        consulta=request.form['inputConsulta'].replace('/r','')
        consulta=re.sub("\r","",consulta)
        consulta=consulta.split('\n')
        print(consulta)
        try:
            englishText=translate(consulta)
            print(englishText)
            data['español']=consulta
            data['ingles']=englishText
            r=requests.get('http://localhost:3000/awesomeAigment')
            objects=getEntitiesAllClefSpanish(englishText,consulta)
            data['objects']=objects
            atomos=validar(objects)
            data['atomos']=atomos
        except (Exception) as error :
            print(error)
            return render_template('error.html',error=error)
        return render_template('respuesta.html',data=data)
    return render_template('formulario.html')

if __name__ == "__main__":
    app.run(debug=True,port="5000")