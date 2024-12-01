from glob import glob
from collections import defaultdict
from pprint import pp
from content import get_content
from ask_user import ask_user_bin, get_keywords_from_user


def detect_files(config):
    """Fonction qui détecte les fichiers du type spécifié dans config et retourne leurs chemins

    Args:
        search_path (str): Le chemin du répertoire de recherche
        file_type (str, optional): Le format à rechercher. Defaults to ".txt".

    Returns:
        list[str]: La liste des chemins des fichiers valides
    """
    
    fichiers_trouves = glob(config.search_path+"/**/*"+config.filetype)
    
    config.fichiers = fichiers_trouves
    
def retrieve(config) -> set | defaultdict[str,list[str]]:
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
    
    
    while config.keywords:
        pertinents_keywords = set() # set des fichiers de l'ensemble de mots-clé actuel
        for query in config.keywords:
        
            pertinents_query = set() # set des fichiers du mot-clé actuel
            for file in config.fichiers:
                try:
                    content:str = get_content(file)
                except Exception as e:
                    print(f'Exception {e}; fichier: {file}')
                    continue
                    
                if contains(content, query):
                    pertinents_query.update([file])
                    results_queries[query].append(file)
            
            pertinents_keywords.update(pertinents_query)
            all_pertinents.update(pertinents_query)
        
        pp(pertinents_keywords) 
        
        config.keywords = get_keywords_from_user("Autres mots-clés ? (mots-clés pour chercher / entrée pour sortir)\n")
        
    pp(dict(results_queries))
    
    config.all_results.update(all_pertinents)
    config.resultats_queries.update(results_queries)

#############################################################

def contains(content:str, query:str) -> bool:
    """Vérifie si le fichier contient le mot-clé

    Args:
        doc (str): le contenu (texte) du fichier
        query (str): le mot-clé
    
    Idées:
        méthodes plus sophistiquées (vectorisation par ex)
        séparer traitement fichier txt et fichier pdf
    """
    return query in content
    
    
