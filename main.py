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

for concept in root.findall('.//skos:Concept', namespaces):
    prefLabelText = ""
    for prefLabel in concept.findall('.//skos:prefLabel', namespaces):
        print(prefLabel.text)
        prefLabelText = prefLabel.text.replace(" ", "%20").replace("'", "%27").replace("(", "%28").replace(")", "%29").replace("/", "%2F").replace(",", "%2C")

    for attrib in concept.attrib:
        concept.attrib[attrib] = 'http://my.site.com/#'+prefLabelText
    print(concept.attrib)
#print(e)

tree.write('skos.rdf')