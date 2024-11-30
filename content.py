import json
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.high_level import extract_pages



def get_content(file:str) -> str:
    
    if file.endswith(".txt") or file.endswith(".md") or file.endswith(".py"):
        return get_content_txt(file)
    elif file.endswith(".pdf"):
        return get_content_pdf(file)
    elif file.endswith(".ipynb"):
        return get_content_ipynb(file)
    
def get_content_txt(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def get_content_pdf(file): 
    """
    file: le chemin du fichier
    """

    full_text = ""
    with open(file, 'rb') as file:
        for page_layout in extract_pages(file, page_numbers=[0]):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().lower()
                    full_text += text
                    
    return full_text

def get_content_ipynb(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    text = ""
    for cell in content['cells']:
        text += "".join(cell["source"])
    return text
