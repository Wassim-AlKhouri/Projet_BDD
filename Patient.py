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

def UpdateMedecin(newmedecin):
    cursor.execute("""UPDATE Patient SET
                              (medecinDeReferenceINAMI)
                              VALUES (%s)""",
                              (newmedecin)
                            )
def UpdatePharmacien(newpharmacien):
    cursor.execute("""UPDATE Patient SET
                              (medecinDeReferenceINAMI)
                              VALUES (%s)""",
                              (newpharmacien)
                            )
def MedicalInformations(NISS):
    cursor.execute(""" SELECT * FROM patient p WHERE p.NISS = VALUES (%s) """,(NISS))
    cursor.execute(""" SELECT * FROM diagnostique WHERE p.NISS = VALUES (%s) """,(NISS))
    
def Traitement(NISS):
    cursor.execute(""" SELECT dp.medicamentNomCommercial, dp.DCI, dp.datePrescription, dp.dateVente, dp.dureeTraitement FROM DossierPatient dp WHERE dp.NISS = VALUES (%s) """,(NISS))



