import re
import math
import json
import operator
from collections import Counter
import collections
from lxml import etree as ET
import urllib.request
import urllib.parse
import csv


def complete_concept(concept, row, count):
    french_term = row[0]
    note_1 = row[1]
    english_term = row[2]
    note_2 = row[3]
    note_3 = row[4]
    note_4 = row[5]
    if french_term.endswith(' '):
        french_term = french_term[:-1]
    if english_term.endswith(' '):
        english_term = english_term[:-1]

    # If the English term has a French matching and the French term doesn't exist in the skos file
    if french_term != "" and len(concept.findall(
            '{http://www.w3.org/2004/02/skos/core#}prefLabel[@{http://www.w3.org/XML/1998/namespace}lang=\'fr-FR\']',
            namespaces)) == 0:
        french_pref_label = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}prefLabel')
        french_pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "fr-FR"
        french_pref_label.text = french_term

    # If there is a note 1 to add :
    if note_1 != "":
        note_1_elemen = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}scopeNote')
        note_1_elemen.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "fr-FR"
        note_1_elemen.text = "Sources bibliographiques des termes français : " + note_1

    # If there is a note 2 to add :
    if note_2 != "":
        note_2_elemen = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}scopeNote')
        note_2_elemen.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "fr-FR"
        note_2_elemen.text = "Progression de la validation : " + note_2

    # If there is a note 3 to add :
    if note_3 != "":
        note_3_elemen = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}scopeNote')
        note_3_elemen.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "fr-FR"
        note_3_elemen.text = "Commentaires : " + note_3

    # If there is a note 4 to add :
    if note_4 != "":
        note_4_elemen = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}scopeNote')
        note_4_elemen.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "fr-FR"
        note_4_elemen.text = "Sources bibliographiques des termes anglais : " + note_4


tree = ET.parse('workingDirectory/skos_Internationalized.rdf')
root = tree.getroot()

namespaces = {"skos": "http://www.w3.org/2004/02/skos/core#",
              "xml": "http://www.w3.org/XML/1998/namespace",
              "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

noTDTR = []
count = 0
countLog = []
notFoundInSkos = []
notFoundInSkosNoTerm = []
with open('workingDirectory/toAddContent.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    # For each line of the csv file:
    for row in spamreader:
        # Incrementing counter
        count += 1
        foundInSkos = False
        # Defining properties
        frenchTerm = row[0]
        note1 = row[1]
        englishTerm = row[2]
        note2 = row[3]
        note3 = row[4]
        note4 = row[5]
        if frenchTerm.endswith(' '):
            frenchTerm = frenchTerm[:-1]
        if englishTerm.endswith(' '):
            englishTerm = englishTerm[:-1]

        # We loop the Skos file to find a matching between the CSV line and a Skos:Concept
        for concept in root.findall('.//skos:Concept', namespaces):
            for elem in list(concept.iter()):
                # If we find a matching for an English term:
                if (elem.tag == '{http://www.w3.org/2004/02/skos/core#}prefLabel') \
                        and (elem.text == englishTerm) \
                        and (count not in countLog)\
                        and elem.get('{http://www.w3.org/XML/1998/namespace}lang') == "en-UK":
                    # Script variables
                    countLog.append(count)
                    foundInSkos = True

                    # If the English term is not validated
                    if note1.find("TDTR") == -1:
                       noTDTR.append("ERROR : " + str(count) + " > " + elem.text + " <> " + englishTerm + " => " + note1)

                    # Printing logs for user
                    print(str(count) + " > " + elem.text + " <> " + englishTerm + " => " + note1 + " fr: " + frenchTerm)
                    complete_concept(concept, row, count)

        if foundInSkos is False:
            # If an English term exists:
            if englishTerm != "":
                notFoundInSkos.append("NEW ENGLISH TERM : " + str(count) + " > " + englishTerm)
                # Creation of the skos:Concept element:
                concept = ET.SubElement(root, '{http://www.w3.org/2004/02/skos/core#}Concept')
                concept.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] = "http://my.site.com/#"+urllib.parse.quote(englishTerm).replace('/', '%2F')

                # Creation of the English term:
                englishPrefLabel = ET.SubElement(concept, '{http://www.w3.org/2004/02/skos/core#}prefLabel')
                englishPrefLabel.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "en-UK"
                englishPrefLabel.text = englishTerm

                complete_concept(concept, row, count)
            # Else if there is a French term
            elif englishTerm == "" and frenchTerm != "":
                notFoundInSkos.append("NEW FRENCH TERM : " + str(count) + " > " + frenchTerm)

                # Creation of the skos:Concept element:
                concept = ET.SubElement(root, '{http://www.w3.org/2004/02/skos/core#}Concept')
                concept.attrib[
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] = "http://my.site.com/#fr-" + urllib.parse.quote(
                    frenchTerm).replace('/', '%2F')

                complete_concept(concept, row, count)
            # Else, we raise an error
            else:
                notFoundInSkosNoTerm.append("notFoundInSkosNoTerm : " + str(count) + " > " + str(row))

print("New terms :")
for i in notFoundInSkos:
    print(i)

print("No term :")
for i in notFoundInSkosNoTerm:
    print(i)

print("No TDTR :")
for i in noTDTR:
    print(i)

tree.write('workingDirectory/skos_toImport.rdf')
