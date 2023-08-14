from static.python.consumingNER import candidates
import spacy
import re
import pandas as pd
from itertools import zip_longest
def get_word(string, pos):
    for i, m in enumerate(re.finditer('[A-Za-z0-9\-\,#\$\á\é\í\ó\ú\"\'@%&\(\)\:\/]+', string)):
        if m.end()>=pos:
            return i
def getSpanishAlignment(line):
    line = line.split()
    df = pd.DataFrame(columns=['spa', 'eng'])
    for element in line:
        spa, eng = element.split("-")
        new_row = {'spa':int(spa), 'eng':int(eng)}
        df = df._append(new_row, ignore_index=True)
    return df
def getProjection(cadenaEN, cadenaES, alineamiento, iniEnt, finEnt):
    nlp = spacy.load("en_core_web_sm")
    nlpES = spacy.load("es_core_news_sm")
    docCadenaEN = nlp(cadenaEN)
    docCadenaES=nlpES(cadenaES)
    dicCadenaES=dict(zip(range(len(docCadenaES)), docCadenaES))
    dicCadenaEN=dict(zip(range(len(docCadenaEN)), docCadenaEN))
    df = getSpanishAlignment(alineamiento)
    cadenaObjetivo=cadenaEN[iniEnt:finEnt]
    docCadenaObjetivo = nlp(cadenaObjetivo)
    locationCadena=get_word(cadenaEN, iniEnt)
    dicCadenaObjetivo={k: v for k,v in list(enumerate(docCadenaObjetivo,locationCadena))}
    dfResultantes = pd.DataFrame(columns=['spa', 'eng'])
    for key, value in dicCadenaObjetivo.items():
        dfResultantes = pd.concat([dfResultantes, df.query("eng == @key",inplace=False)], axis=0)
    cadena=[]
    dfResultantes.sort_values(by=['spa'], inplace=True)
    print(dfResultantes)
    for index, row in dfResultantes.iterrows():
        cadena.append(str(dicCadenaES[ row['spa']]))
    statement = " ".join(cadena)
    return statement
def getEntitiesAllClefSpanish(englishText,spanishText):
    nlpEN = spacy.load("en_core_web_sm")
    nlpES = spacy.load("es_core_news_sm")
    fileObjects = open('./static/data/objects.txt', 'w', encoding='utf-8')
    count = 0
    objects = []
    candidatos=[]
    z = list(zip_longest(spanishText,englishText))
    for line1,line2 in z:
        print("line1: "+ str(line1))
        print("line2: "+ str(line2))
        print("line2: "+line2 +" line1: "+ line1)
        docCadenaEN = nlpEN(line2)
        docCadenaES = nlpES(line1)
        line1= ' '.join([token.text_with_ws for token in docCadenaES])
        line1 = re.sub("  ", " ", line1)
        line2= ' '.join([token.text_with_ws for token in docCadenaEN])
        line2 = re.sub("  ", " ", line2)
        candidate=[]
        alignment = getAlignment(count)
        candidate = candidates(line2)
        for data in candidate:
            alineado = getProjection(line2, line1, alignment, data['start'], data['finish'])
            pattern = '\s*[\,\.\-\)\()]*$|^\s*[\,\.\)\-\()]'
            phrase = re.sub(pattern, '', data['phrase'])
            alineado = re.sub(pattern, '', alineado)
            score =0
            if phrase is None or phrase =="":
                phrase = " ";
            if (len(data['cui'])==0 or isinstance(data['cui'], str)):
                fileObjects.write(line1+"~"+data['cui']+"~"+phrase+"~"+alineado+"~"+str(data['start'])+"~"+str(data['finish'])+"~"+str(data['score'])+"\n" )
                objects.append([data['cui'],phrase,alineado,str(data['start']),str(data['finish']),str(data['score'])])
            else:
                for cui in data['cui']:
                    cuiStrip=re.sub("UMLS/",  "",  cui)
                    fileObjects.write(line1+"~"+cuiStrip+"~"+alineado+"~"+phrase+"~"+str(data['start'])+"~"+str(data['finish'])+"~"+str(data['score'])+"\n" )
                    objects.append([cuiStrip,phrase,alineado,str(data['start']),str(data['finish']),str(data['score'])])
        candidatos.append(candidate)
        count =count+1
        print("line: "+ str(count))
    fileObjects.close()
    print(objects)
    return objects
def getAlignment(numLine):
    file = open('./static/data/output.txt', 'r', encoding='utf-8')
    content = file.readlines()
    return content[numLine]