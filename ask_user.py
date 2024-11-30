from ouvrir import ouvrir

MULTI_ENTRY_SEP = "," 
NEGATIVE_OR_EXIT_RESPONSES = ["exit", "e", "n", ""]
def is_exit_response(response):
    return response in NEGATIVE_OR_EXIT_RESPONSES

def ask_user_bin(question, pos_rep="y"):
    return input(question) == pos_rep


def ask_user_fichiers(config):
    reponse = input("Ouvrir les fichiers ? (y/n/N°requete(s)):\n")
    if reponse.isalpha():
        
        if not is_exit_response(reponse):
            ouvrir(config.all_results, config.filetype)
        else:
            exit()            
    else :
        
        try:
            # Séparer l'entrée si c'est une liste d'indices
            indices = reponse.split(MULTI_ENTRY_SEP)  
            # Convertir chaque élément en entier
            indices = [int(i) for i in indices]
        
            resultat_ouvrir = set()
            
            for i in indices:
                _, files = list(config.resultats_queries.items())[i]
                resultat_ouvrir.update(files)
            
            if resultat_ouvrir:
                ouvrir(resultat_ouvrir, config.filetype)  # Ouvrir les fichiers sélectionnés
            else:
                print("Aucun fichier valide sélectionné.")

        except ValueError as e:
            print(f"Erreur <{e}>\nEntrée non valide, veuillez entrer un ou plusieurs indices numériques.")

def get_keywords_from_user():
    keywords_input:list[str] = input(f"Mots-clés 'mot1{MULTI_ENTRY_SEP}mot2...' : \n")
    keywords = [kw.strip() for kw in keywords_input.split(MULTI_ENTRY_SEP)]
    return keywords

def get_arguments_from_user():
    filetype = keywords = None
    search_path:str = input("Chemin dans lequel rechercher : \n")
    
    if search_path != '': 
        filetype:str = input("Type de fichiers : \n")
        keywords:list[str] = get_keywords_from_user()
    return search_path, filetype, keywords
    
def ask_user_config():
    return input('\n=>Que voulez-vous faire ?\nr: recherche | i: info | a: addrac | s: supprac | h: help | e: exit\n') 
