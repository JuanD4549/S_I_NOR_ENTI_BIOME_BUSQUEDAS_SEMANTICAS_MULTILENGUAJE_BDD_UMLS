import requests
import xml.etree.ElementTree as ET
import re

def getResults(xml):
    root = ET.fromstring(xml)
    results = []
    for phrase in root.findall('.//Phrase'):
        start=phrase.find('./PhraseStartPos').text
        lenght=phrase.find('./PhraseLength').text
        for candidate in phrase.findall('./Mappings/Mapping/MappingCandidates/Candidate'):
            score=candidate.find('./CandidateScore').text
            cui = candidate.find('./CandidateCUI').text
            label = candidate.find('./CandidatePreferred').text
            phraseText =  phrase.find('./PhraseText').text
            PARAMS = {'data':cui}
            r=requests.post('http://localhost:80/crosswalk', data=PARAMS)
            snomedids = r.content
            if len(snomedids) == 0:
                results.append({'cui': cui, 'label': label, 'snomedid': 'not found', 'phrase': phraseText, 'score':score, 'start':int(start), 'finish':int(start) + int(lenght) })
            else:
                r=requests.post('http://localhost:80/crosswalk', data=PARAMS)
                snomedids = r.content
                for snomedid in snomedids:
                    if cui is None or cui == "":
                        cont = 9
                    else:
                        results.append({'cui': cui, 'label': label, 'snomedid': snomedid, 'phrase': phraseText, 'score':score, 'start':int(start), 'finish':int(start) + int(lenght)})
    uniqR = {v['cui']:v for v in results}.values()
    return uniqR
def remove_namespace(tree):
    """
    Strip namespace from parsed XML
    """
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith("{")
        except AttributeError:
            continue  # node.tag is not a string (node is a comment or similar)
        if has_namespace:
            node.tag = node.tag.split("}", 1)[1]
            #print(attributes["grp"])
def candidates(linea):
   #input  = request.form['data']
   PARAMS = {'data':linea}
   r=requests.post('http://localhost:80/metamap', data=PARAMS)
   #tree = ElementTree.fromstring(r.content)
   data = r.content.decode("utf-8")
   dict = []
   if data is not None and data != "":
        string = re.sub("<\?xml.*\?>", "", data)
        string = re.sub("<!DOCTYPE.*dtd\"\>", "", string)
        #string = re.sub(r"\\n", "", data) 
        #parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        #h = fromstring(string, parser=parser)
        response = {}
        try:
            response = getResults(string)
        except Exception:
            cont = 0
        for i in response:
            dict.append(i)
   return dict
