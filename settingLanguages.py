import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos_urise.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

for concept in root.findall('.//skos:Concept', namespaces):
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}prefLabel':
            newElem = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}narrower')
            elem.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "en-UK"
            print(elem)

tree.write('workingDirectory/skos_toImport.rdf')