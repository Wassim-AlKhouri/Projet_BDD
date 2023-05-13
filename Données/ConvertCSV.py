import csv
import mysql.connector
import os
from datetime import datetime

def convert_date(date):
    date_obj = datetime.strptime(date, '%m/%d/%Y')
    date_formatted = date_obj.strftime('%Y-%m-%d')
    return date_formatted



cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost',
    database='groupAX_DB'

)
cursor = cnx.cursor()
path = "D:\documents\GitHub\Projet_BDD\Données Projet-20230426\pathologies.csv"
root_name = os.path.splitext(os.path.basename(path))[0]
with open(path,'r', encoding="utf-8") as file:
    csvreader = list(csv.reader(file))
    if (root_name == "dossiers_patients"):
        categorie = csvreader[0]
        cat = ",".join(categorie) 
        for row in csvreader[1:]:
            values = list(row)
            values[7] = convert_date(values[7])
            values[8] = convert_date(values[8])
            cursor.execute("""INSERT INTO DossierPatient 
                            (NISS,medecinNom,medecinINAMI,pharmacienNom,pharmacienINAMI,medicamentNomCommercial,DCI,datePrescription,dateVente,dureeTraitement) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (values))
    elif( root_name == "medicaments"):
        categorie = csvreader[0]
        cat = ",".join(categorie) 
        for row in csvreader[1:]:
            values = list(row)
            cursor.execute("""INSERT INTO Medicament 
                           (DCI,medicamentNomCommercial,systèmeAnatomiqueNom,conditionnement) 
                           VALUES(%s,%s,%s,%s)""",
                           (values))
    elif( root_name == "pathologies"):
        for row in csvreader:
            values = list(row)
            try:
                cursor.execute("""INSERT INTO Pathologie 
                                (pathologieNom, specialiteNom) 
                                VALUES(%s,%s)""",
                                (values))
            except(mysql.connector.errors.IntegrityError):
                print("duplicate entry for pathologieNom: " + values[0] + " and specialiteNom: " + values[1])
    cnx.commit()
    cursor.close()
    cnx.close()

