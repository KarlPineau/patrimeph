import re
import math
import json
import operator
from collections import Counter
import collections
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

tree = ET.parse('skos.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

arrayNamespace = []
arrayFalse = []

for preConcept in root.findall('.//skos:Concept', namespaces):
    for preAttrib in preConcept.attrib:
        arrayNamespace.append(preConcept.attrib[preAttrib])


for broader in root.findall('.//skos:broader', namespaces):
    for attrib in broader.attrib:
        if broader.attrib[attrib] not in arrayNamespace:
            arrayFalse.append(" > broader > "+broader.attrib[attrib])
for narrower in root.findall('.//skos:narrower', namespaces):
    for attrib in narrower.attrib:
        if narrower.attrib[attrib] not in arrayNamespace:
            arrayFalse.append(" > narrower > "+narrower.attrib[attrib])
for related in root.findall('.//skos:related', namespaces):
    for attrib in related.attrib:
        if related.attrib[attrib] not in arrayNamespace:
            arrayFalse.append(" > related > "+related.attrib[attrib])

print(arrayNamespace)
for error in arrayFalse:
    print(error)
