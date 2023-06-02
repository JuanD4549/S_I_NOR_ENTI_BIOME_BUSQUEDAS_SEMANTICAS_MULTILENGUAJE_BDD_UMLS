from libretranslatepy import LibreTranslateAPI

if __name__ == '__main__':
    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    fileES = open('spanish.txt', 'r', encoding='utf-8')
    fileEN = open('ingles.txt', 'w', encoding='utf-8')

    Lines = fileES.readlines()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        lineText = line.split("|||")
        count += 1
        print("Line{}: {}".format(count, lineText[1].strip()))
        lineEN = lt.translate(lineText[1], "es", "en")
        print("Line{}: {}".format(count, lineEN.strip()))
        fileEN.write(lineText[0]+"|||"+lineEN)
        #
    fileES.close()
    fileEN.close()
    
