import argparse

from config import Config, SUPPORTED_FILETYPES
from menu import Menu
from ask_user import ask_user_fichiers

#######################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rechercher des fichiers à partir de mots-clés. Pour sortir d'un menu, il est possible d'appuyer simplement sur 'entrée'")
    parser.add_argument('-i', '--info', action='store_true', help="Affiche les types de fichiers supportés et les raccourcis")
    parser.add_argument('-a', '--addrac', action='store_true', help="Ajouter un raccourci")
    parser.add_argument('-s', '--supprac', action='store_true', help="Supprimer un raccourci")
    parser.add_argument("search_path",nargs='?' , type=str, help="Le chemin où effectuer la recherche\n Format: Avec slashs ou antislashs et avec ou sans cotes. Pour le redo, ecrire sans les cotes") #et si on a besoin des cotes dans le redo (path avec espace) ?
    parser.add_argument("filetype", nargs='?', type=str, default=".txt", help=f"Un type de fichier à rechercher. Peut-être {SUPPORTED_FILETYPES}.")
    parser.add_argument('keywords', nargs='*', type=str, help="Une liste de mots-clés à rechercher. Introduire des mots-clés séparés par des espaces") # Et comment on fait si on veut mettre des le debut des mots cles multitermes ?
    #args = parser.parse_args()
    
    config = Config() 
    menu = Menu(parser, config)
    
    menu.run()
    


## Add

# Vérifier les askusers cas particuliers

# prendre en compte nom du fichier, surtout quand on en a bcp (unlikely, il faudrait soit vectoriser, vaut pas le coup, soit list de mots et non)?
# Ajouter en Comm le fait que si on a -i le prgrm quitte immédiatement, et que les raccourcis doivent être écris en majuscule
# Ouvrir les fichiers selon le numero de requête (jpense il faut des classes)
# Peut être sauvegarder l'emplacement où le mot-clé a été trouvé et proposer d'afficher une fenêtre autour (ptet un argument optionnel qui affiche la phrase dans laquelle se trouve le mot à la fin de la recherche)
# Dans l'exécution avec le raccourci, mettre soit des commandes spéciales, soit un mot-clé qui emmene vers un menu des actions spéciales (aide, voir les raccourcis etc)
# Verifier le cas de plusieurs recherche, entre si c'est demandé dans la fonction retrieve ou dans le menu principal