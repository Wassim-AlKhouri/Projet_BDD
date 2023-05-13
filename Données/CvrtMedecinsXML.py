import xml.etree.ElementTree as ET
import os
"""import mysql.connector"""

"""cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost'
    database='groupAX_DB'
)"""

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
root = tree.getroot()

for child in root.findall('medecin'):
    inami = child.find('inami').text
    mail = child.find('mail').text
    nom = child.find('nom').text
    specialite = child.find('specialite').text
    telephone = child.find('telephone').text

    print("inami:", inami)
    print("mail:", mail)
    print("nom", nom)
    print("specialite:", specialite)
    print("telephone:", telephone)

