from ouvrir import ouvrir
from icecream import ic

def ask_user_bin(question, pos_rep="y"):
    return input(question) == pos_rep


def ask_user_fichiers(config):
    reponse = input("Ouvrir les fichiers ? (y/n/N°requete(s)):\n")
    if reponse.isalpha():
        ic("alpha")
        if reponse == "n":
            exit()
        else:
            ouvrir(config.all_results, config.filetype)
            
    else :
        #ic("not alpha")
        try:
            # Séparer l'entrée si c'est une liste d'indices
            indices = reponse.replace(",", " ").split()  
            # Convertir chaque élément en entier
            indices = [int(i) for i in indices]
            #ic(indices)
            resultat_ouvrir = set()
            
            for i in indices:
                _, files = list(config.resultats_queries.items())[i]
                resultat_ouvrir.update(files)
            #ic(resultat_ouvrir)
            if resultat_ouvrir:
                ouvrir(resultat_ouvrir, config.filetype)  # Ouvrir les fichiers sélectionnés
            else:
                print("Aucun fichier valide sélectionné.")

        except ValueError as e:
            print(f"Erreur <{e}>\nEntrée non valide, veuillez entrer un ou plusieurs indices numériques.")
