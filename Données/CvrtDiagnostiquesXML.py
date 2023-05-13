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
for child in root.findall('diagnostique'):
    NISS = child.find('NISS').text
    date_diagnostic = child.find('date_diagnostic').text
    naissance = child.find('naissance').text
    pathology = child.find('pathology').text
    specialite = child.find('specialite').text

    print("NISS:", NISS)
    print("Date du diagnostic:", date_diagnostic)
    print("Date de naissance:", naissance)
    print("Pathologie:", pathology)
    print("Spécialité:", specialite)
    print("===============================")


