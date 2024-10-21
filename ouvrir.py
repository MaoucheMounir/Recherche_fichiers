import subprocess

def ouvrir(fichiers:set, filetype):
    if filetype == ".txt":
        ouvrir_txt(fichiers)
    elif filetype == ".pdf":
        ouvrir_pdf(fichiers)
    elif filetype == ".md" or filetype == ".py" or filetype == ".ipynb":
        ouvrir_code(fichiers)

def ouvrir_txt(fichiers):
    for fichier in fichiers:
        subprocess.Popen(["notepad.exe", fichier])

def ouvrir_pdf(fichiers):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe" #Attention cette inst peut être source de bug
    for fichier in fichiers:
        subprocess.Popen([chrome_path, fichier])

def ouvrir_code(fichiers):
    code_path = r"C:\Microsoft VS Code\bin\Code.cmd" #J'aurais pu mettre \vscode\code.exe mais celle-là est mieux
    for fichier in fichiers:
      subprocess.Popen([code_path, fichier]) # subprocess.run n'a pas fonctionné.
