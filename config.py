import os
import raccourcis as rc
from pprint import pp

supported_filetypes = [".txt", ".pdf", ".md", ".py", ".ipynb"]


class Config():

    def __init__(self, search_path=None, filetype=None, keywords=None):
        self.search_path:str = search_path
        self.filetype:str = filetype
        self.keywords:list[str] = keywords
        self.raccourcis = rc.load_raccourcis()
        
        self.fichiers:list[str] = None
        self.all_results:set[str] = None
        self.resultats_queries:dict[str, list[str]] = None
    
    
    ################################
    
    def set_retrieval_params(self, search_path, filetype, keywords):
        self.search_path:str = search_path
        self.filetype:str = filetype
        self.keywords:list[str] = keywords
        
        del self.fichiers, self.all_results
    
    ################################
    
    def verify_filetype(self):
        if not self.filetype.startswith("."):
            value = "." + self.filetype
        else:
            value = self.filetype
            
        while value not in supported_filetypes+["exit"]:
            value = input(f"Type de fichier non supporté. Choisissez parmi {supported_filetypes} sinon tapez 'exit'.")
        
        if value == "exit":
            exit()
        else:
            self.filetype = value
            

    def verify_path(self):
        value = self.raccourcis.get(self.search_path, self.search_path)
        
        while not (os.path.exists(value) or value in self.raccourcis or value == 'exit'):
            value = input(f"Chemin inexistant. Réessayez ou quittez ('exit').")
            
        if value == "exit":
            exit()
        else:
            self.search_path = self.raccourcis.get(value, value)
            

    def verify_default(self):
        return not (self.search_path=="C:/_Cours/_M1-S2" and self.filetype==".txt" and self.keywords==[]) ## If the user didn't specify anything
            
        
        
    def verify_inputs(self):
        self.verify_default()
        self.verify_filetype()
        self.verify_path()
    
    ###########################
    
    def print_info(self):
        print("Types de fichiers supportés: ", *supported_filetypes)
        print("Raccourcis:")
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
        