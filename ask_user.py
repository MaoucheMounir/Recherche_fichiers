from ouvrir import ouvrir
from icecream import ic

MULTI_ENTRY_SEP = "," 


def ask_user_bin(question, pos_rep="y"):
    return input(question) == pos_rep


def ask_user_fichiers(config):
    reponse = input("Ouvrir les fichiers ? (y/n/N°requete(s)):\n")
    if reponse.isalpha():
        
        if reponse == "n":
            exit()
        else:
            ouvrir(config.all_results, config.filetype)
            
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


def get_arguments_from_user():
    
    search_path:str = input("Chemin dans lequel rechercher : \n")
    filetype:str = input("Type de fichiers : \n")
    keywords:list[str] = input(f"Mots-clés 'mot1{MULTI_ENTRY_SEP}mot2...' : \n").split(",")
    
    return search_path, filetype, keywords
    
    
