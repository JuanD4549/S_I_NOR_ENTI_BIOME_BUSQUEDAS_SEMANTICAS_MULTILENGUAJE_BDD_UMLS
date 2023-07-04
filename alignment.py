import spacy
import re
import pandas as pd
import consumingNER
#import googleNLP
from itertools import zip_longest, count
def get_word(string, pos):
    for i, m in enumerate(re.finditer('[A-Za-z0-9\-\,#\$\á\é\í\ó\ú\"\'@%&\(\)\:\/]+', string)):
        if m.end()>=pos:
            return i
def getSpanishAlignment(line):
    #line = line.strip().split("\t")
    #line[1] = line[1].split()
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
    #print(df)
    #cadenaObjetivo=cadena[7:15]
    cadenaObjetivo=cadenaEN[iniEnt:finEnt]
    docCadenaObjetivo = nlp(cadenaObjetivo)
    locationCadena=get_word(cadenaEN, iniEnt)
    
    dicCadenaObjetivo={k: v for k,v in list(enumerate(docCadenaObjetivo,locationCadena))}
    #print("cadenaObjetivo", cadenaObjetivo)
    #print("cadenaObjetivoDic", dicCadenaObjetivo)
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
def getEntitiesAllClef(labeler):
    nlpEN = spacy.load("en_core_web_sm")
    nlpES = spacy.load("es_core_news_sm")
    fileObjects = open('objects.txt', 'w', encoding='utf-8')
    count = 0
    candidates=[]
    with open('spanish.txt', 'r', encoding='utf-8') as f1, open('ingles.txt', 'r', encoding='utf-8') as f2:
        z = list(zip_longest(f1,f2))
        for line1,line2 in z:
            spanish = line1.split("|||")
            english = line2.split("|||")
            docCadenaEN = nlpEN(english[1])
            docCadenaES = nlpES(spanish[1])
            line1= ' '.join([token.text_with_ws for token in docCadenaES])
            line1 = re.sub("  ", " ", line1)
            line2= ' '.join([token.text_with_ws for token in docCadenaEN])
            line2 = re.sub("  ", " ", line2)
            candidate=[]
            alignment = getAlignment(count)
            #if labeler == "google":
            #    candidate= googleNLP.googlenlp(line2)
            if labeler=="metamap":
                candidate = consumingNER.candidates(line2)
            for data in candidate:
                #print(data['phrase'])
                alineado = getProjection(line2, line1, alignment, data['start'], data['finish'])
                #alineado = getProjection("- reduction in the production of hematites ( aplastic anaemia )", "- reducción de la producción de hematíes ( anemia aplásica )", "0-0 3-3 5-5 6-6 10-10 9-8 4-4 7-7 8-9 2-2 1-1", 43, 61)
                #fileObjects.write(spanish[0]+"|||"+data['cui']+"|||"+data['phrase']+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"|||"+line2+"|||"+line1+alignment )
                pattern = '\s*[\,\.\)\()]*$|^\s*[\,\.\)\()]'
                phrase = re.sub(pattern, '', data['phrase'])
                if phrase is None or phrase =="":
                    phrase = " ";
                if (len(data['cui'])==0):
                    fileObjects.write(spanish[0]+"|||"+data['cui']+"|||"+phrase+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" )
                #elif (len(data['cui'])==1):
                #    fileObjects.write(spanish[0]+"|||"+data['cui'][0]+"|||"+phrase+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" )
                else:
                    for cui in data['cui']:
                        cuiStrip=re.sub("UMLS/",  "",  cui)
                        fileObjects.write(spanish[0]+"|||"+cuiStrip+"|||"+phrase+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" )
                #fileObjects.write(spanish[0]+"|||"+phrase+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" ) 
                #print(alineado)
            candidates.append(candidate)
            count =count+1
            print("line: "+ str(count))
    fileObjects.close()
def getEntitiesAllClefSpanish(labeler):
    nlpEN = spacy.load("en_core_web_sm")
    nlpES = spacy.load("es_core_news_sm")
    fileObjects = open('objects.txt', 'w', encoding='utf-8')
    count = 0
    candidates=[]
    with open('spanish.txt', 'r', encoding='utf-8') as f1, open('ingles.txt', 'r', encoding='utf-8') as f2:
        z = list(zip_longest(f1,f2))
        for line1,line2 in z:
            spanish = line1.split("|||")
            english = line2.split("|||")
            docCadenaEN = nlpEN(english[1])
            docCadenaES = nlpES(spanish[1])
            line1= ' '.join([token.text_with_ws for token in docCadenaES])
            line1 = re.sub("  ", " ", line1)
            line2= ' '.join([token.text_with_ws for token in docCadenaEN])
            line2 = re.sub("  ", " ", line2)
            candidate=[]
            alignment = getAlignment(count)
            #if labeler == "google":
            #    candidate= googleNLP.googlenlp(line2)
            if labeler=="metamap":
                candidate = consumingNER.candidates(line2)
            for data in candidate:
                #print(data['phrase'])
                alineado = getProjection(line2, line1, alignment, data['start'], data['finish'])
                #alineado = "  "
                #alineado = getProjection("- reduction in the production of hematites ( aplastic anaemia )", "- reducción de la producción de hematíes ( anemia aplásica )", "0-0 3-3 5-5 6-6 10-10 9-8 4-4 7-7 8-9 2-2 1-1", 43, 61)
                #fileObjects.write(spanish[0]+"|||"+data['cui']+"|||"+data['phrase']+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"|||"+line2+"|||"+line1+alignment )
                pattern = '\s*[\,\.\-\)\()]*$|^\s*[\,\.\)\-\()]'
                phrase = re.sub(pattern, '', data['phrase'])
                alineado = re.sub(pattern, '', alineado)
                score =0
                
                if phrase is None or phrase =="":
                    phrase = " ";
                if (len(data['cui'])==0 or isinstance(data['cui'], str)):
                    
                    fileObjects.write(spanish[0]+"~"+data['cui']+"~"+phrase+"~"+alineado+"~"+str(data['start'])+"~"+str(data['finish'])+"~"+str(data['score'])+"\n" )
                #elif (len(data['cui'])==1):
                #    fileObjects.write(spanish[0]+"|||"+data['cui'][0]+"|||"+phrase+"|||"+"sin alingnment"+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" )
                else:
                    for cui in data['cui']:
                        cuiStrip=re.sub("UMLS/",  "",  cui)
                        fileObjects.write(spanish[0]+"~"+cuiStrip+"~"+phrase+"~"+alineado+"~"+str(data['start'])+"~"+str(data['finish'])+"~"+str(data['score'])+"\n" )
                #fileObjects.write(spanish[0]+"|||"+phrase+"|||"+alineado+"|||"+str(data['start'])+"|||"+str(data['finish'])+"\n" ) 
                #print(alineado)
            candidates.append(candidate)
            count =count+1
            print("line: "+ str(count))
    fileObjects.close()
def getAlignment(numLine):
    file = open('output.txt', 'r', encoding='utf-8')
    content = file.readlines()
    return content[numLine]
if __name__ == "__main__":
   #cadena = "I have headache."
   #cadenaES="tengo dolor de cabeza."
   #alineamiento="1\t0-1 1-2 2-2 3-2 4-3"
   #alignment(cadena, cadenaES,alineamiento, 0, 6)
   #getEntitiesAllClef("google")
   getEntitiesAllClefSpanish("metamap")
   