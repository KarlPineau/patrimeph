import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos_completed.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

listMatches = []

for concept in root.findall('.//skos:Concept', namespaces):
    uri = concept.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')

    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}altLabel' or elem.tag == '{http://www.w3.org/2004/02/skos/core#}prefLabel':
            language = elem.get("{http://www.w3.org/XML/1998/namespace}lang")
            filterListMatches = list(filter(lambda match: match['label'] == elem.text and match['language'] == language and match['uri'] != uri, listMatches))
            if len(filterListMatches) > 0:
                print(filterListMatches)
                elem.text = elem.text+" 2"
            else:
                match = {"label": elem.text, "language": language, "uri": uri}
                listMatches.append(match)

tree.write('workingDirectory/skos_toImport.rdf')
