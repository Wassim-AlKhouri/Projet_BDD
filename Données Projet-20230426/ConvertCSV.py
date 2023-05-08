import csv
import mysql.connector
import os

cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost',
    database='groupAX_DB'

)
path = "./dossiers_patients.csv"
root_name = os.path.splitext(os.path.basename(path))[0]
with open(path,'r', encoding="utf-8") as file:
    csvreader = list(csv.reader(file))
    if (root_name == "dossiers_patients"):
        categorie = list(csvreader)[1:]
        cat = ",".join(categorie) 
        for row in csvreader[1:]:
            values = ",".join(row)
            cursor.execute("INSERT INTO dossier_patients (%s) VALUES(%s)",(cat,values)) 
            cnx.commit
    elif( root_name == "medecins"):
        categorie = list(csvreader)[1:]
        cat = ",".join(categorie) 
        for row in csvreader[1:]:
            values = ",".join(row)
            cursor.execute("INSERT INTO medecins (dci,nom Commercial,système anatomique,conditionnement) VALUES(%s)",(values)) 
            cnx.commit
    elif( root_name == "pathologies"):
        for row in csvreader:
            values = ",".join(row)
            cursor.execute("INSERT INTO dossier_patients (maladie, domaine_maladie) VALUES(%s)",(values)) 
            cnx.commit

