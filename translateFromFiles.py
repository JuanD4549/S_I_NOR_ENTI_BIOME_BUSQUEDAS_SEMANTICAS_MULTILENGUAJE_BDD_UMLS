from libretranslatepy import LibreTranslateAPI

if __name__ == '__main__':
    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    fileES = open('spanish.txt', 'r', encoding='utf-8')
    fileEN = open('ingles.txt', 'w', encoding='utf-8')

    Lines = fileES.readlines()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        
        count += 1
        #print("Line{}: {}".format(count, lineText[1].strip()))
        #print("Line{}: {}".format(count))
        #lineEN = lt.translate(lineText[1], "es", "en")
        lineEN = lt.translate(line,"es", "en")
        print("Line{}: {}".format(count, lineEN.strip()))
        #fileEN.write(lineText[0]+"|||"+lineEN)}
        fileEN.write(lineEN)

    fileES.close()
    fileEN.close()
    
