import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('workingDirectory/skos_without_duplicates.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

URI = []
doneDuplicate = []

for concept in root.findall('.//skos:Concept', namespaces):
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}NT':
            URILabel = urllib.parse.quote(elem.text)
            URI = "http://my.site.com/#" + URILabel
            newElem = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}narrower')
            newElem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = URI
            print(URI)
        elif elem.tag == '{http://www.w3.org/2004/02/skos/core#}RT':
            URILabel = urllib.parse.quote(elem.text)
            URI = "http://my.site.com/#" + URILabel
            newElem = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}related')
            newElem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = URI
            print(URI)
        elif elem.tag == '{http://www.w3.org/2004/02/skos/core#}BT':
            URILabel = urllib.parse.quote(elem.text)
            URI = "http://my.site.com/#" + URILabel
            newElem = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}broader')
            newElem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = URI
            print(URI)

for concept in root.findall('.//skos:Concept', namespaces):
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}NT':
            concept.remove(elem)
        elif elem.tag == '{http://www.w3.org/2004/02/skos/core#}RT':
            concept.remove(elem)
        elif elem.tag == '{http://www.w3.org/2004/02/skos/core#}BT':
            concept.remove(elem)

error = []
for concept in root.findall('.//skos:Concept', namespaces):
    for elem in list(concept.iter()):
        if elem.tag == '{http://www.w3.org/2004/02/skos/core#}related':
            attrib = elem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
            findConcept = root.findall('.//skos:Concept[@rdf:about="'+attrib+'"]', namespaces)
            if len(findConcept) == 0:
                elem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = attrib.replace("%0A%20%20%20%20%20%20%20%20%20%20%20%20", "%20")
                error.append(attrib)

tree.write('workingDirectory/skos_toImport.rdf')
print(error)