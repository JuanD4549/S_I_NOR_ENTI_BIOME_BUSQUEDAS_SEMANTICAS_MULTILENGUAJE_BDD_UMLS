from libretranslatepy import LibreTranslateAPI

def translate(spanishText):
    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    englishText=[]
    fileEngSpn = open('./static/data/EngSpn.txt', 'w', encoding='utf-8')
    # Strips the newline character
    count=0
    #print(total)
    for line in spanishText:
        #print("Line{}: {}".format(count, lineText[1].strip()))
        #print("Line{}: {}".format(count))
        #lineEN = lt.translate(lineText[1], "es", "en")
        englishText.append(lt.translate(line,"es", "en"))
        fileEngSpn.write(line+" ||| "+englishText[count]+"\n" )
        count+=1
    fileEngSpn.close()
    #print(englishText)
    return englishText

