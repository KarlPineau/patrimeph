# Ginco Encoder
L'objectif de ce repository est d'encoder des fichiers skos de manière à les rendre comptatible avec le logiciel Ginco

La procédure d'encodage est la suivante :
- Déposer le fichier skos à encoder dans le dossier **workingDirectory**
- Renommer le fichier en **skos.rdf**
- Ouvrir le fichier **skos.rdf**. S'il ne contient pas de balise *skos:ConceptScheme* :
    - Lancer Ginco
    - Créer un nouveau thésaurus sur Ginco, remplir les champs obligatoires avec des valeurs quelconques
    - Exporter le thésaurus nouvellement créé au format skos
    - Supprimer le thésaurus créé sur Ginco
    - Renommer le fichier obtenu en **thesaurus.rdf**, le placer dans **workingDirectory**
    - Pour lire les fichiers RDF, utiliser le logiciel Oxygen : http://www.oxygenxml.com/
    - Copier l'intégralité des balises skos:Concept du **skos.rdf** dans le fichier **thesaurus.rdf**, entre la dernière balise *owl:ObjectProperty* et la balise *skos:ConceptScheme*
    - Supprimer le fichier **skos.rdf**
    - Renommer **thesaurus.rdf** en **skos.rdf**
- Exécuter **main.py** Ce fichier a pour objectif de réécrire les URI internes au fichier 
- Exécuter **lookForErrors.py** : Ce fichier cherche les URI orphelines dans le fichier. Il est nécessaire de résoudre ces dernières (en les supprimant ou en les modifiant) avant de continuer. 
- Exécuter **mergeDuplicate.py** : Ce fichier a pour objectif de supprimer les doublons de concept
- Exécuter **lookForErrorsAlt.py** : Ce fichier retourne les alt qui seraient présents en doublon dans le fichier, ce qui est interdit par Ginco. Il faut les modifier ou les supprimer.
- Exécuter **uriseTermes.py** : Ce Fichier a pour objectif de rajouter des URI aux Concepts
- Le fichier obtenu est dénommé **sko_toImport.rdf**, il ne reste plus qu'à l'importer dans Ginco