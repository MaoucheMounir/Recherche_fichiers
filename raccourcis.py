import os
import pickle

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
