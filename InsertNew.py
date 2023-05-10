import mysql.connector
#from datetime import datetime
import csv
cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost',
        database='groupAX_DB'
    )
cursor = cnx.cursor()

def insertNewPatient(NISS,DateNaissance,genre,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI,nom,prenom):
    cursor.execute("""INSERT INTO Patient 
                              (NISS,DateNaissance,genre,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI,nom,prenom)
                              VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                              (NISS,DateNaissance,genre,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI,nom,prenom)
                            )

def insertNewPharmacien(INAMI,mail,employeNom,employeNum):
    cursor.execute("""INSERT INTO Pharmacien 
                            (INAMI,employeNom,employeNum) 
                            VALUES (%s,%s,%s)""",
                            (INAMI,employeNom,employeNum)
                          )
    if mail is not None:
      cursor.execute("""INSERT INTO EmployeEmail 
                        (INAMI,email)
                        VALUES (%s,%s)""",
                        (INAMI,mail)
                      )   

def insertNewMedecin(INAMI,mail,employeNom,employeNum,specialite):
    cursor.execute("""INSERT INTO medecin 
                              (INAMI,employeNom,employeNum,specialite)
                              VALUES (%s,%s,%s,%s)""",
                              (INAMI,employeNom,employeNum,specialite)
                            )
    if mail is not None :
      cursor.execute("""INSERT INTO EmployeEmail 
                        (INAMI,mail)
                        VALUES (%s,%s)""",
                        (INAMI,mail)
                      )
