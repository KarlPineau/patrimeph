import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('skos_without_duplicates.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

arrayAlt = []
arrayFalse = []

#for preAlt in root.findall('.//skos:altLabel', namespaces):
#    if preAlt.text in arrayAlt:
#        arrayFalse.append(preAlt.text)
#    else:
#        arrayAlt.append(preAlt.text)


for concept in root.findall('.//skos:Concept', namespaces):
    arrayAltConcept = []
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}altLabel':
            if elem.text not in arrayAltConcept:
                if elem.text in arrayAlt:
                    arrayFalse.append(elem.text)
                else:
                    arrayAlt.append(elem.text)
                arrayAltConcept.append(elem.text)

print(arrayFalse)
