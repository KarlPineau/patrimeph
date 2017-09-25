import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos_toImport.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

arrayAlt = []
arrayFalse = []

for concept in root.findall('.//skos:Concept', namespaces):
    arrayAltConcept = []
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}altLabel' or elem.tag == '{http://www.w3.org/2004/02/skos/core#}prefLabel':
            if elem.text not in arrayAltConcept:
                if elem.text in arrayAlt:
                    arrayFalse.append(elem.text)
                else:
                    arrayAlt.append(elem.text)
                arrayAltConcept.append(elem.text)

print(arrayFalse)

for toRemove in arrayFalse:
    for concept in root.findall('.//skos:Concept', namespaces):
        for elem in list(concept.iter()):
            if elem.tag == '{http://www.w3.org/2004/02/skos/core#}altLabel' or elem.tag == '{http://www.w3.org/2004/02/skos/core#}prefLabel':
                if elem.text == toRemove:
                    if len(concept.findall('{http://www.w3.org/2004/02/skos/core#}prefLabel', namespaces)) == 1:
                        root.remove(concept)
                        print("1: " + toRemove)
                    else:
                        concept.remove(elem)
                        print("2: "+toRemove)


tree.write('workingDirectory/skos_toImport_test.rdf')
