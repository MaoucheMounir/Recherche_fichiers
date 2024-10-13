import os
import argparse
import subprocess
from collections import defaultdict
from pprint import pp
import pickle
import json

from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.high_level import extract_pages

global filetype 
global supported_filetypes
global raccourcis
supported_filetypes = [".txt", ".pdf", ".md", ".py", ".ipynb"]



############################################################

def explore(search_path, file_type=".txt"):
    """Fonction qui récupère les chemins des fichiers correspondant à l'extension et se trouvant dans search_path

    Args:
        search_path (str): Le chemin du répertoire de recherche
        file_type (str, optional): Le format à rechercher. Defaults to ".txt".

    Returns:
        list[str]: La liste des chemins des fichiers valides
    """
    
    fichiers_trouves = []
    
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(file_type):
                fichiers_trouves.append(os.path.join(root, file))
    
    return fichiers_trouves
    
def retrieve(fichiers:list[str], keywords:list[str]) -> set[str]:
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
        for query in keywords:
        
            pertinents_query = set() # set des fichiers de la requête actuelle
            for file in fichiers:
                content = get_content(file)
                if contains(content, query):
                    pertinents_query.update([file])
                    results_queries[query].append(file)
            
            all_pertinents.update(pertinents_query)
        
        pp(pertinents_query)
        
        if redo:=ask_user_bin("Autre requête ? (y/n):\n"):
            keywords = input('Donnez un ou des mots-clé "mot1,mot2,...":\n').split(sep=',')
    
    pp(dict(results_queries))
    return all_pertinents


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
    

#################################

def get_content_txt(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def get_content_pdf(file): 
    """
    file: le chemin du fichier
    """

    full_text = ""
    with open(file, 'rb') as file:
        for page_layout in extract_pages(file, page_numbers=[0]):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().lower()
                    full_text += text
                    
    return full_text

def get_content(file):
    
    if file.endswith(".txt") or file.endswith(".md"):
        return get_content_txt(file)
    elif file.endswith(".pdf"):
        return get_content_pdf(file)
    elif file.endswith(".ipynb"):
        return get_content_ipynb(file)
    
def get_content_ipynb(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    text = ""
    for cell in content['cells']:
        text += "".join(cell["source"])
    return text

####################################

def verify_filetype():
    global filetype
    value = filetype
    
    if not value.startswith("."):
        value = "." + filetype
    
    while value not in supported_filetypes+["exit"]:
        value = input(f"Type de fichier non supporté. Choisissez parmi {supported_filetypes} sinon tapez 'exit'.")
    
    if value == "exit":
        exit()
    else:
        filetype = value

def verify_path():
    global search_path
    value = raccourcis.get(search_path, search_path)
    
    while not (os.path.exists(value) or value == 'exit'):
        value = input(f"Chemin inexistant, réessayez ou quittez ('exit').")
        
    if value == "exit":
        exit()
    else:
        search_path = value
        
def ask_user_bin(question, pos_rep="y"):
    return input(question) == pos_rep

####################################

def ouvrir(fichiers:dict):
    global filetype
    
    if filetype == ".txt":
        ouvrir_txt(fichiers)
    elif filetype == ".pdf":
        ouvrir_pdf(fichiers)
    elif filetype == ".md" or filetype == ".py" or filetype == ".ipynb":
        
        ouvrir_md(fichiers)

def ouvrir_txt(fichiers):
    for fichier in fichiers:
            subprocess.Popen(["notepad.exe", fichier])

def ouvrir_pdf(fichiers):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe" #Attention cette inst peut être source de bug
    for fichier in fichiers:
        subprocess.Popen([chrome_path, fichier])

def ouvrir_md(fichiers):
    code_path = r"C:\Microsoft VS Code\bin\Code.cmd" #J'aurais pu mettre \vscode\code.exe mais celle-là est mieux
    for fichier in fichiers:
      subprocess.Popen([code_path, fichier]) # subprocess.run n'a pas fonctionné.


######################################

def print_info():
    global supported_filetypes
    global raccourcis
    
    print("Types de fichiers supportés: ", *supported_filetypes)
    print("Raccourcis:")
    pp(raccourcis)

def add_raccourci(chemin, id):
    global raccourcis
    
    raccourcis[id] = chemin
    
    store_raccourcis(raccourcis)
    
def supp_raccourci(id):
    global raccourcis
    del raccourcis[id]
    
    store_raccourcis(raccourcis)

def store_raccourcis(raccourcis):
    with open("raccourcis.pkl", "wb") as f:
        pickle.dump(raccourcis, f)

def load_raccourcis():
    if os.path.exists("raccourcis.pkl"):
        with open("raccourcis.pkl", "rb") as f:
            raccourcis = pickle.load(f)
    else:
        raccourcis = {}
        
    return raccourcis

#######################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rechercher des fichiers à partir de mots-clés")
    parser.add_argument('-i', '--info', action='store_true', help="Affiche les types de fichiers supportés et les raccourcis")
    parser.add_argument('-a', '--addrac', action='store_true', help="Ajouter un raccourci")
    parser.add_argument('-s', '--supprac', action='store_true', help="Supprimer un raccourci")
    parser.add_argument("filetype", nargs='?', type=str, default=".txt", help=f"Un type de fichier à rechercher. Peut-être {supported_filetypes}.")
    parser.add_argument("search_path",nargs='?' , type=str, default="C:/_Cours/_M1-S2", help="Le chemin où effectuer la recherche\n Format: Avec slashs ou antislashs et avec ou sans cotes. Pour le redo, ecrire sans les cotes") #et si on a besoin des cotes dans le redo (path avec espace) ?
    parser.add_argument('keywords', nargs='*', type=str, help="Une liste de mots-clés à rechercher. Introduire des mots-clés séparés par des espaces") # Et comment on fait si on veut mettre des le debut des mots cles multitermes ?
    
    
    args = parser.parse_args()
    
    filetype = args.filetype
    search_path = args.search_path
    keywords = args.keywords
    #info = args.info
    
    raccourcis = load_raccourcis()
    
    if args.addrac:
        chemin = r'' + input("Donner un chemin:\n")
        id = input('Donner un identifiant\n')
        add_raccourci(chemin, id)
        exit()

    if args.supprac:
        id = input('Donner un identifiant\n')
        supp_raccourci(id)
        exit()
    
    if args.info:
        print_info()
        exit()
    else:
        if search_path=="C:/_Cours/_M1-S2" and filetype==".txt" and keywords==[]: ## If the user didn't specify anything
            exit()
    
    ## Verifier les inputs
    verify_filetype()
    verify_path()
    
    ## Effectuer la recherche
    fichiers = explore(search_path, filetype)
    resultat = retrieve(fichiers, keywords)
    
    ## Ouvrir les fichiers
    if len(resultat) > 0 and ask_user_bin("Ouvrir les fichiers ? (y/n/N°requete):\n"):
        ouvrir(resultat)


## Add
# optional arguments better in terminal?
# get content md files
# prendre en compte nom du fichier, surtout quand on en a bcp (unlikely, il faudrait soit vectoriser, vaut pas le coup, soit list de mots et non)?
# Ajouter en Comm le fait que si on a -i le prgrm quitte immédiatement, et que les raccourcis doivent être écris en majuscule
# recherceh dans fichier python aussi
# Ouvrir les fichiers selon le numero de requête (jpense il faut des classes)
# Peut être sauvegarder l'emplacement où le mot-clé a été trouvé et proposer d'afficher une fenêtre autour (ptet un argument optionnel qui affiche la phrase dans laquelle se trouve le mot à la fin de la recherche)