from libretranslatepy import LibreTranslateAPI

def translate(spanishText):
    #cargamos la api necesaria para la traduccion
    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    englishText=[]
    fileEngSpn = open('./static/data/EngSpn.txt', 'w', encoding='utf-8')
    count=0
    #se le cada uno de la linea de texto ingresadas
    for line in spanishText:
        #Inica el proceso de traduccion
        englishText.append(lt.translate(line,"es", "en"))
        fileEngSpn.write(line+" ||| "+englishText[count]+"\n" )
        count+=1
    fileEngSpn.close()
    #retorna el texto traducido al ingles
    return englishText

