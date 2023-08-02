from time import sleep
from libretranslatepy import LibreTranslateAPI
from tqdm import tqdm

def translate(spanishText):
    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    englishText=[]
    fileEngSpn = open('similarity/awesome-align/EngSpn.txt', 'w', encoding='utf-8')
    # Strips the newline character
    count=0
    total=len(spanishText)
    #print(total)
    with tqdm(100) as pbar:
        for line in spanishText:
            #print("Line{}: {}".format(count, lineText[1].strip()))
            #print("Line{}: {}".format(count))
            #lineEN = lt.translate(lineText[1], "es", "en")
            englishText.append(lt.translate(line,"es", "en"))
            fileEngSpn.write(line+" ||| "+englishText[count]+"\n" )
            count+=1
            pbar.update((count*100)/total)
    fileEngSpn.close()
    print(englishText)
    return englishText

