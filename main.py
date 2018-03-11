import re
import math
import json
import operator
from collections import Counter
import collections
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

for concept in root.findall('.//skos:Concept', namespaces):
    prefLabelText = ""
    for prefLabel in concept.findall('.//skos:prefLabel', namespaces):
        print(prefLabel.text)
        prefLabelText = urllib.parse.quote(prefLabel.text).replace('/', '%2F')

    for attrib in concept.attrib:
        concept.attrib[attrib] = 'https://patrimeph.huma-num.fr/#'+prefLabelText
    print(concept.attrib)

tree.write('workingDirectory/skos.rdf')