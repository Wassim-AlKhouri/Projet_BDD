import csv
import mysql.connector
import os

cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost'
)
path = "./dossiers_patients.csv"
root_name = os.path.splitext(os.path.basename(path))[0]
with open(path,'r', encoding="utf-8") as file:
    csvreader = list(csv.reader(file))
    categorie = list(csvreader)[1:]
    if (root_name == "dossiers_patients"):
        for row in csvreader[1:]:
            cursor.execute("INSERT INTO dossier_patients (%s) VALUES(%i,%s,%i,%s,%s,%s,%s,%s,%s,%s)",(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])) 
            db.commit
    elif( root_name == "medecins"):
        for row in csvreader[1:]:
            cursor.execute("INSERT INTO medecins (dci,nom Commercial,système anatomique,conditionnement) VALUES(%s,%s,%s,%s)",(row[0],row[1],row[2],row[3])) 
            db.commit
    elif( root_name == "pathologies"):
        for row in csvreader:
            cursor.execute("INSERT INTO dossier_patients (maladie, domaine_maladie) VALUES(%s,%s)",(row[0],row[1])) 
            db.commit

