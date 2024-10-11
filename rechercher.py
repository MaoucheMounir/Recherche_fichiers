import os
import argparse
import subprocess
from collections import defaultdict

from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.high_level import extract_pages

global filetype 
global supported_filetypes
supported_filetypes = [".txt", ".pdf", ".md"]

raccourcis = {'M1S2': r"C:\_Cours\_M1-S2", 
              "M1S1": r"C:\_Cours\_M1-S1", 
              "M2S1": r"C:\_Cours\__M2-S2",
              "ML":   r"C:\_Cours\_M1-S2\_ML",
              "RITAL":r"C:\_Cours\_M1-S2\_RITAL",
              "PIMA": r"C:\_Cours\M1-S2\_PIMA"}

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
    

def get_content_txt(file):
    with open(file, "r") as f:
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
    print(file)
    if file.endswith(".txt") or file.endswith(".md"):
        return get_content_txt(file)
    elif file.endswith(".pdf"):
        return get_content_pdf(file)

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
        
        print(pertinents_query)
        
        if redo:=ask_user_bin("Autre requête ? (y/n):\n"):
            keywords = input('Donnez un ou des mots-clé "mot1,mot2,...":\n').split(sep=',')
    
    print(dict(results_queries))
    return all_pertinents



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

def ouvrir(fichiers:dict):
    global filetype
    if filetype == ".txt":
        ouvrir_txt(fichiers)
    elif filetype == ".pdf":
        ouvrir_pdf(fichiers)

def ouvrir_txt(fichiers):
    for fichier in fichiers:
            subprocess.Popen(["notepad.exe", fichier])

def ouvrir_pdf(fichiers):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe" #Attention cette inst peut être source de bug
    for fichier in fichiers:
        subprocess.Popen([chrome_path, fichier])

def ouvrir_md(fichiers):
    code_path = r"C:\Microsoft VS Code\Code.exe" #Attention cette inst peut être source de bug
    for fichier in fichiers:
        subprocess.Popen([code_path, fichier])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rechercher des fichiers à partir de mots-clés")
    parser.add_argument("filetype", type=str, default=".txt", help=f"Un type de fichier à rechercher. Peut-être {supported_filetypes}.")
    parser.add_argument("search_path", type=str, default="C:/_Cours/_M1-S2", help="Le chemin où effectuer la recherche\n Format: Avec slashs ou antislashs et avec ou sans cotes. Pour le redo, ecrire sans les cotes") #et si on a besoin des cotes dans le redo (path avec espace) ?
    parser.add_argument('keywords', nargs='+', type=str, help="Une liste de mots-clés à rechercher. Introduire des mots-clés séparés par des espaces") # Et comment on fait si on veut mettre des le debut des mots cles multitermes ?
    args = parser.parse_args()
    
    filetype = args.filetype
    search_path = args.search_path
    keywords = args.keywords
    
    ## Verifier les inputs
    verify_filetype()
    verify_path()
    
    ## Effectuer la recherche
    fichiers = explore(search_path, filetype)
    resultat = retrieve(fichiers, keywords)
    
    ## Ouvrir les fichiers
    if len(resultat) > 0 and ask_user_bin("Ouvrir les fichiers ? (y/n):\n"):
        ouvrir(resultat)


## Add
# optional arguments better in terminal?
# get content md files
# prendre en compte nom du fichier, surtout quand on en a bcp (unlikely, il faudrait soit vectoriser, vaut pas le coup, soit list de mots et non)?
