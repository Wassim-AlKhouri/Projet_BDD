import xml.etree.ElementTree as ET
import os
import mysql.connector
from datetime import datetime
import csv
############################ BASIC ###################################################################################

def convert_date(date):
    date_obj = datetime.strptime(date, '%m/%d/%Y')
    date_formatted = date_obj.strftime('%Y-%m-%d')
    return date_formatted

############################ XML ####################################################################################


def creat_root_for_xml(path):
    try:
        tree = ET.parse(path)
    except : 
        root_name = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'r') as f:
            data = f.read()

        with open(path, 'w') as f:
            f.write("<"+root_name+">\n" + data + "\n</"+ root_name+">")
            f.close()
        #tree = ET.parse(path)


def insert_diagnostiques(path,cursor):
    creat_root_for_xml(path)
    for event, diagnostique in ET.iterparse(path):
        if diagnostique.tag == "diagnostique":
            NISS = diagnostique.find('NISS').text
            dateDiagnostic = diagnostique.find('date_diagnostic').text
            dateDiagnostic_formatted = convert_date(dateDiagnostic)
            dateNaisseance = diagnostique.find('naissance').text
            dateNaisseance_formatted = convert_date(dateNaisseance)
            pathologieNom = diagnostique.find('pathology').text
            specialiteNom = diagnostique.find('specialite').text
            cursor.execute("""INSERT INTO Diagnostic 
                              (NISS,dateDiagnostic,dateNaisseance,pathologieNom,specialite) 
                              VALUES (%s,%s,%s,%s,%s)""",
                              (NISS,dateDiagnostic_formatted,dateNaisseance_formatted,pathologieNom,specialiteNom)
                            )


def insert_pharmacien(path,cursor):
    creat_root_for_xml(path)
    for event, pharmacien in ET.iterparse(path):
        if pharmacien.tag == "pharmacien":
            INAMI = pharmacien.find('inami').text
            employeNom = pharmacien.find('nom').text
            employeNum = pharmacien.find('tel').text
            cursor.execute("""INSERT INTO Pharmacien 
                              (INAMI,employeNom,employeNum) 
                              VALUES (%s,%s,%s)""",
                              (INAMI,employeNom,employeNum)
                            )
            email_elment = pharmacien.find('mail')
            if email_elment is not None and email_elment.text is not None:
                email = email_elment.text
                cursor.execute("""INSERT INTO EmployeEmail 
                                  (INAMI,email)
                                  VALUES (%s,%s)""",
                                  (INAMI,email)
                                )
            
            
def insert_medecin(path,cursor):
    creat_root_for_xml(path)
    for event, medecin in ET.iterparse(path):
        if medecin.tag == "medecin":
            INAMI = medecin.find('inami').text
            employeNom = medecin.find('nom').text
            employeNum = medecin.find('telephone').text
            specialite = medecin.find('specialite').text
            cursor.execute("""INSERT INTO medecin 
                              (INAMI,employeNom,employeNum,specialite)
                              VALUES (%s,%s,%s,%s)""",
                              (INAMI,employeNom,employeNum,specialite)
                            )
            email_elment = medecin.find('mail')
            if email_elment is not None and email_elment.text is not None:
                email = email_elment.text
                cursor.execute("""INSERT INTO EmployeEmail 
                                  (INAMI,email)
                                  VALUES (%s,%s)""",
                                  (INAMI,email)
                                )
                
            
def insert_patient(path,cursor):
    creat_root_for_xml(path)
    for event, patient in ET.iterparse(path):
        if patient.tag == "patient":
            NISS = patient.find('NISS').text
            DateNaissance = patient.find('date_de_naissance').text
            DateNaissance_formatted = convert_date(DateNaissance)
            genre = patient.find('genre').text
            medecinDeReferenceINAMI = patient.find('inami_medecin').text
            pharmacienDeReferenceINAMI = patient.find('inami_pharmacien').text
            nom = patient.find('nom').text
            prenom = patient.find('prenom').text
            cursor.execute("""INSERT INTO Patient 
                              (NISS,DateNaissance,genre,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI,nom,prenom)
                              VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                              (NISS,DateNaissance_formatted,genre,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI,nom,prenom)
                            )
            email_elment = patient.find('mail')
            if email_elment is not None and email_elment.text is not None:
                email = email_elment.text
                cursor.execute("""INSERT INTO patientEmail 
                                  (NISS,email)
                                  VALUES (%s,%s)""",
                                  (NISS,email)
                                )
            numeroGSM_elment = patient.find('telephone')
            if numeroGSM_elment is not None and numeroGSM_elment.text is not None:
                numeroGSM = numeroGSM_elment.text
                cursor.execute("""INSERT INTO patientGSM 
                                  (NISS,numeroGSM)
                                  VALUES (%s,%s)""",
                                  (NISS,numeroGSM)
                                )
                

def insert_specialite(path,cursor):
    creat_root_for_xml(path)
    for event, specialite in ET.iterparse(path):
        if specialite.tag == "specialite":
            specialiteNom = specialite.find('name').text
            cursor.execute("""INSERT INTO Specialite 
                              (specialiteNom) 
                              VALUES (%s)""",
                              (specialiteNom,)
                            )
            for systèmeAnatomiqueNom in specialite.iter('medicament'):
                systèmeAnatomiqueNom = systèmeAnatomiqueNom.text
                cursor.execute("""INSERT INTO SpecialiteSystèmeAnatomique 
                                (systèmeAnatomiqueNom, specialiteNom) 
                                VALUES (%s,%s)""",
                                (systèmeAnatomiqueNom, specialiteNom)
                                )
            

############################# CSV ###################################################################################


def insert_csv(path,cursor):
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


############################# MAIN ###################################################################################


if __name__ == "__main__":
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost',
        database='groupAX_DB'
    )
    cursor = cnx.cursor()
    #insert_diagnostiques("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\diagnostiques.xml",cursor)
    #insert_pharmacien("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\pharmaciens.xml",cursor)
    #insert_medecin("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\medecins.xml",cursor)
    #insert_patient("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\patients.xml",cursor)
    #insert_specialite("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\specialites.xml",cursor)
    #insert_csv("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\dossiers_patients.csv",cursor)
    #insert_csv("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\medicaments.csv",cursor)
    #insert_csv("D:\documents\GitHub\Projet_BDD\Données Projet-20230426\pathologies.csv",cursor)

    ### TESTING ###
    cursor.execute("""SELECT s.specialiteNom
                    FROM Specialite s
                    JOIN SpecialiteSystèmeAnatomique a ON s.specialiteNom = a.SpecialiteNom
                    JOIN Medicament m ON m.systèmeAnatomiqueNom=a.systèmeAnatomiqueNom
                    JOIN DossierPatient d ON d.medicamentNomCommercial=m.medicamentNomCommercial
                    GROUP BY s.specialiteNom
                    ORDER BY COUNT(*) DESC
                    LIMIT 1;""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("Number of rows: %s" % cursor.rowcount)

    cnx.commit()
    cursor.close()
    cnx.close()