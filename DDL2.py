import mysql.connector

cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost'
)

# Create a new database if it doesn't exist
cursor = cnx.cursor()
try:
    cursor.execute("CREATE DATABASE groupAX_DB")
except mysql.connector.errors.DatabaseError as err:
    if err.errno == mysql.connector.errorcode.ER_DB_CREATE_EXISTS:
        print("Database already created or a database with the same name exists")
        print("Would you like to drop the database and create a new one? (y/n)")
        if input() == 'y':
            cursor.execute("DROP DATABASE groupAX_DB")
            cursor.execute("CREATE DATABASE groupAX_DB")
        else:
            print("Aborting")
            exit(1)
    else:
        print(err.msg)
        exit(1)
        
cursor.execute("USE groupAX_DB")

cursor.execute("""CREATE TABLE Specialite (specialiteNom VARCHAR(50) PRIMARY KEY)""")

cursor.execute("""CREATE TABLE SpecialiteSystemeAnatomique (
                systemeAnatomiqueNom VARCHAR(50) NOT NULL,
                specialiteNom VARCHAR(50) NOT NULL REFERENCES Specialite(specialiteNom),
                PRIMARY KEY (systemeAnatomiqueNom, specialiteNom)
                )""")

cursor.execute("""CREATE TABLE Pathologie (
                pathologieNom VARCHAR(50) PRIMARY KEY,
                specialiteNom VARCHAR(50) NOT NULL REFERENCES Specialite(specialiteNom)
                )""")

cursor.execute("""CREATE TABLE Medicament (
                DCI VARCHAR(50),
                systemeAnatomiqueNom VARCHAR(50),
                medicamentNomCommercial VARCHAR(50) NOT NULL,
                conditionnement INT NOT NULL,
                PRIMARY KEY (medicamentNomCommercial, conditionnement)
                )""")

cursor.execute("""CREATE TABLE Employe (
                INAMI DECIMAL(12,0) PRIMARY KEY,
                employeNom VARCHAR(50) NOT NULL,
                employeNum VARCHAR(20) NOT NULL
                )""")

cursor.execute("""CREATE TABLE EmployeEmail (
                INAMI DECIMAL(12,0) NOT NULL REFERENCES Employe(INAMI),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (INAMI, email)
                )""")

cursor.execute("CREATE TABLE Medecin LIKE Employe")

cursor.execute("ALTER TABLE Medecin ADD specialite VARCHAR(50) NOT NULL REFERENCES Specialite(specialiteNom)")

cursor.execute("CREATE TABLE Pharmacien LIKE Employe")

cursor.execute("""CREATE TABLE Patient (
                NISS DECIMAL(12,0) PRIMARY KEY,
                DateNaissance DATE NOT NULL,
                genre SMALLINT NOT NULL,
                medecinDeReferenceINAMI DECIMAL(12,0) NOT NULL REFERENCES Medecin(INAMI),
                pharmacienDeReferenceINAMI DECIMAL(12,0) NOT NULL REFERENCES Pharmacien(INAMI),
                nom VARCHAR(50) NOT NULL,
                prenom VARCHAR(50) NOT NULL
                )""")

cursor.execute("""CREATE TABLE PatientEmail (
                NISS DECIMAL(12,0) NOT NULL REFERENCES Patient(NISS),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (NISS) 
                )""")

cursor.execute("""CREATE TABLE PatientGSM (
                NISS DECIMAL(12,0) NOT NULL REFERENCES Patient(NISS),
                numeroGSM VARCHAR(20) NOT NULL,
                PRIMARY KEY (NISS)
                )""")

cursor.execute("""CREATE TABLE DossierPatient (
                NISS DECIMAL(12,0) REFERENCES Patient(NISS),
                medecinNom VARCHAR(50) NOT NULL,
                medecinINAMI DECIMAL(12,0) NOT NULL REFERENCES Medecin(INAMI),
                pharmacienNom VARCHAR(50) NOT NULL,
                pharmacienINAMI DECIMAL(12,0) NOT NULL REFERENCES Pharmacien(INAMI),
                medicamentNomCommercial VARCHAR(50) NOT NULL,
                DCI VARCHAR(50) NOT NULL,
                datePrescription DATE NOT NULL,
                dateVente DATE NOT NULL,
                dureeTraitement INT NOT NULL,
                Primary Key (NISS,  medecinINAMI, medicamentNomCommercial, datePrescription)
                )""")

cursor.execute("""CREATE TABLE Diagnostic (
                NISS DECIMAL(12,0) NOT NULL REFERENCES Patient(NISS),
                dateDiagnostic DATE NOT NULL,
                dateNaisseance DATE NOT NULL,
                pathologieNom VARCHAR(50) NOT NULL REFERENCES Pathologie(pathologieNom),
                specialite VARCHAR(50) NOT NULL REFERENCES Specialite(specialiteNom),
                PRIMARY KEY (NISS, pathologieNom, dateDiagnostic)
                )""")


# Commit the changes and close the cursor and connection objects
cnx.commit()
cursor.close()
cnx.close()
print("Database created successfully")