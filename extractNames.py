import re
import math
import json
import operator
from collections import Counter
import collections
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos_end.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

labels = []
for concept in root.findall('.//skos:Concept', namespaces):
    for prefLabel in concept.findall('.//skos:prefLabel', namespaces):
        labels.append(prefLabel.text)

print(labels)