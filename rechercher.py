import argparse

from config import *
from retrieval import *
from ask_user import *


#######################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rechercher des fichiers à partir de mots-clés")
    parser.add_argument('-i', '--info', action='store_true', help="Affiche les types de fichiers supportés et les raccourcis")
    parser.add_argument('-a', '--addrac', action='store_true', help="Ajouter un raccourci")
    parser.add_argument('-s', '--supprac', action='store_true', help="Supprimer un raccourci")
    #parser.add_argument("search_path",nargs='?' , type=str, default="C:/_Cours/_M1-S2", help="Le chemin où effectuer la recherche\n Format: Avec slashs ou antislashs et avec ou sans cotes. Pour le redo, ecrire sans les cotes") #et si on a besoin des cotes dans le redo (path avec espace) ?
    #parser.add_argument("filetype", nargs='?', type=str, default=".txt", help=f"Un type de fichier à rechercher. Peut-être {supported_filetypes}.")
    #parser.add_argument('keywords', nargs='*', type=str, help="Une liste de mots-clés à rechercher. Introduire des mots-clés séparés par des espaces") # Et comment on fait si on veut mettre des le debut des mots cles multitermes ?
    
    args = parser.parse_args()
    
    config = Config() #args.search_path, args.filetype, args.keywords
    do_retrieve = True
    
    if args.info:
        config.print_info()
        do_retrieve = ask_user_bin("Voulez-vous effectuer une recherche ? (y/n)")
    
    if args.addrac:
        config.addrac()
        do_retrieve = ask_user_bin("Voulez-vous effectuer une recherche ? (y/n)")

    if args.supprac:
        config.supprac()
        do_retrieve = ask_user_bin("Voulez-vous effectuer une recherche ? (y/n)")
        
    
    
    while do_retrieve:
        config.set_retrieval_params(*get_arguments_from_user()) 
        config.verify_inputs()
        
        detect_files(config)
        retrieve(config)
        
        do_retrieve = ask_user_bin("Voulez-vous effectuer une recherche ? (y/n)")
        

    ## Ouvrir les fichiers
    if len(config.all_results) > 0 and config.all_results is not None:
        ask_user_fichiers(config)


## Add

# Vérifier les askusers cas particuliers

# optional arguments better in terminal?
# get content md files
# prendre en compte nom du fichier, surtout quand on en a bcp (unlikely, il faudrait soit vectoriser, vaut pas le coup, soit list de mots et non)?
# Ajouter en Comm le fait que si on a -i le prgrm quitte immédiatement, et que les raccourcis doivent être écris en majuscule
# recherceh dans fichier python aussi
# Ouvrir les fichiers selon le numero de requête (jpense il faut des classes)
# Peut être sauvegarder l'emplacement où le mot-clé a été trouvé et proposer d'afficher une fenêtre autour (ptet un argument optionnel qui affiche la phrase dans laquelle se trouve le mot à la fin de la recherche)
# Dans l'exécution avec le raccourci, mettre soit des commandes spéciales, soit un mot-clé qui emmene vers un menu des actions spéciales (aide, voir les raccourcis etc)