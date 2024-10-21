import os
from collections import defaultdict
from pprint import pp
from content import get_content

from ask_user import ask_user_bin

def explore(config):
    """Fonction qui récupère les chemins des fichiers correspondant à l'extension et se trouvant dans search_path

    Args:
        search_path (str): Le chemin du répertoire de recherche
        file_type (str, optional): Le format à rechercher. Defaults to ".txt".

    Returns:
        list[str]: La liste des chemins des fichiers valides
    """
    
    fichiers_trouves = []
    
    for root, _, files in os.walk(config.search_path):
        for file in files:
            if file.endswith(config.filetype):
                fichiers_trouves.append(os.path.join(root, file))
    
    config.fichiers = fichiers_trouves
    
def retrieve(config):
    """Parcourt les fichiers trouvés et retourne ceux qui contiennent au moins un des mots-clés
    Une recherche est définie par une liste de mots-clés à chercher dans la liste de fichiers.
    Après chaque recherche, on affiche l'ensemble des fichiers contenant au moins un des mot-clés.
    A la toute fin, on affiche les fichiers pertinents par mot-clé.
    
    Args:
        fichiers (list[str]): liste des chemins des fichiers
        keywords (list[str]): liste des mots-clés à chercher
    
    Idées:
        Ranking selon le nb mots-clés contenus et/ou similarité
        Print les pertinents de chaque recherche puis les pertinents toutes recherches confondues
    """
    
    results_queries = defaultdict(list) #dictionnaire contenant la liste des fichiers pour chaque query parmi toutes les recherches
    all_pertinents = set() # set des fichiers de toutes les recherches
    
    redo = True
    
    while redo:
        for query in config.keywords:
        
            pertinents_query = set() # set des fichiers de la requête actuelle
            for file in config.fichiers:
                try:
                    content = get_content(file)
                except Exception as e:
                    print(f'Exception {e}; fichier: {file}')
                    continue
                    
                if contains(content, query):
                    pertinents_query.update([file])
                    results_queries[query].append(file)
            
            all_pertinents.update(pertinents_query)
        
        pp(pertinents_query)
        
        if redo:=ask_user_bin("Autre requête ? (y/n):\n"):
            config.keywords = input('Donnez un ou des mots-clé "mot1,mot2,...":\n').split(sep=',')
    
    pp(dict(results_queries))
    
    config.all_results,  config.resultats_queries = all_pertinents, results_queries

#############################################################

def contains(content:str, query:str) -> bool:
    """Vérifie si le fichier contient le mot-clé

    Args:
        doc (str): le contenu (texte) du fichier
        query (str): le mot-cl&
    
    Idées:
        méthodes plus sophistiquées (vectorisation par ex)
        séparer traitement fichier txt et fichier pdf
    """
    return query in content
    
    
