import xml.etree.ElementTree as ET
import os

path = 'diagnostiques.xml'
try:
    tree = ET.parse(path)
except : 
    root_name = os.path.splitext(os.path.basename(path))[0]
    with open(path, 'r') as f:
        data = f.read()

    with open(path, 'w') as f:
        f.write("<"+root_name+">\n" + data + "\n</"+ root_name+">")
        f.close()
    tree = ET.parse(path)
# On utilise la méthode iterparse pour ne pas charger tout le fichier en mémoire
for event, elem in ET.iterparse(path):

    if elem.tag == "diagnostique":
        # On récupère toutes les données présentes dans l'élément "diagnostique"
        for child in elem:
            tag = child.tag
            value = child.text
            print(f"{tag}: {value}")



