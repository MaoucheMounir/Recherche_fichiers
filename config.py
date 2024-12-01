import os
import raccourcis as rc
from ask_user import is_exit_response, NEGATIVE_OR_EXIT_RESPONSES
from pprint import pp

SUPPORTED_FILETYPES = [".txt", ".pdf", ".md", ".py", ".ipynb"]

class Config():

    def __init__(self, search_path=None, filetype=None, keywords=None):
        self.search_path:str = search_path
        self.filetype:str = filetype
        self.keywords:list[str] = keywords
        self.raccourcis = rc.load_raccourcis()
        
        self.fichiers:list[str] = None
        self.all_results:set[str] = set()
        self.resultats_queries:dict[str, list[str]] = dict()
    
    
    ################################
    
    def set_retrieval_params(self, search_path, filetype, keywords):
        self.search_path:str = search_path
        self.filetype:str = filetype
        self.keywords:list[str] = keywords
        
    ################################
    
    def verify_filetype(self):
        if not self.filetype.startswith("."):
            value = "." + self.filetype
        else:
            value = self.filetype
            
        while value not in SUPPORTED_FILETYPES+NEGATIVE_OR_EXIT_RESPONSES:
            value = input(f"Type de fichier non supporté. Choisissez parmi {SUPPORTED_FILETYPES} sinon tapez 'exit'.")
        
        if not is_exit_response(value):
            self.filetype = value
        else:
            exit()
            

    def verify_path(self):
        value = self.raccourcis.get(self.search_path, self.search_path)
        
        while not (os.path.exists(value) or value in self.raccourcis or is_exit_response(value)):
            value = input(f"Chemin inexistant. Réessayez ou quittez ('exit').")
            
        if not is_exit_response(value):
            self.search_path = self.raccourcis.get(value, value)
        else:
            exit()
            
        
    def verify_inputs(self):
        self.verify_filetype()
        self.verify_path()
    
    ###########################
    
    def print_info(self):
        print("=> Types de fichiers supportés: ", *SUPPORTED_FILETYPES)
        print("=> Raccourcis:")
        pp(self.raccourcis)
    
    ###############################
    
    def addrac(self):
        chemin = r'' + input("Donner un chemin:\n")
        while not os.path.exists(chemin):
            chemin = r'' + input("Donner un chemin valide:\n")
            
        id = input('Donner un identifiant\n')
        self.raccourcis = rc.add_raccourci(self.raccourcis, chemin, id)
        
    
    def supprac(self):
        id = input('Donner un identifiant\n')
        self.raccourcis = rc.supp_raccourci(self.raccourcis, id)
        