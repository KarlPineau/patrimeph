import re
import math
import json
import operator
from collections import Counter
import collections
# import xml.etree.ElementTree as ET
from lxml import etree as ET
import urllib.request
import urllib.parse

tree = ET.parse('skos.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

URI = []
doneDuplicate = []

for concept in root.findall('.//skos:Concept', namespaces):
    for attrib in concept.attrib:
        if concept.attrib[attrib] in URI and concept.attrib[attrib] not in doneDuplicate:
            duplicates = root.findall('.//skos:Concept[@rdf:about="' + concept.attrib[attrib] + '"]', namespaces)
            if len(duplicates) > 1:
                count = 0
                for duplicate in duplicates:
                    if count == 0:
                        goodElement = duplicate
                    if count > 0:
                        child1 = list(duplicate.iter())
                        for elem in child1:
                            if elem.tag != '{http://www.w3.org/2004/02/skos/core#}Concept':
                                print(elem.tag)
                                newElem = ET.SubElement(goodElement, elem.tag)
                                newElem.text = elem.text
                                for elemAttrib in elem.attrib:
                                    newElem.attrib[elemAttrib] = elem.attrib[elemAttrib]
                        duplicate.set('toRemove', 'toRemove')
                    count += 1
                doneDuplicate.append(concept.attrib[attrib])
                print(concept.attrib[attrib])
                break
        else:
            URI.append(concept.attrib[attrib])

for toRemove in root.findall('.//skos:Concept[@toRemove="toRemove"]', namespaces):
    root.remove(toRemove)

tree.write('skos_without_duplicates.rdf')