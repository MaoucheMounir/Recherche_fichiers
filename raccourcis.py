import os
import pickle

def add_raccourci(raccourcis, chemin, id):
    raccourcis[id] = chemin
    store_raccourcis(raccourcis)
    return raccourcis
def supp_raccourci(raccourcis, id):
    del raccourcis[id]
    store_raccourcis(raccourcis)
    return raccourcis

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
