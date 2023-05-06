import mysql.connector

cnx = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost'
)

# Create a new database if it doesn't exist
cursor = cnx.cursor()
cursor.execute("DROP DATABASE IF EXISTS groupAX_DB") # à enlever
try:
    cursor.execute("CREATE DATABASE groupAX_DB")
except mysql.connector.errors.DatabaseError as err:
    if err.errno == mysql.connector.errorcode.ER_DB_CREATE_EXISTS:
        print("Database already created or a database with the same name exists")
    else:
        print(err)
    exit(1)
cursor.execute("USE groupAX_DB")

cursor.execute("""CREATE TABLE SystèmeAnatomique (
                systèmeAnatomiqueNom VARCHAR(50) PRIMARY KEY
                )""")

cursor.execute("""CREATE TABLE Pathologie (
                pathologieNom VARCHAR(50) PRIMARY KEY,
                systèmeAnatomiqueNom VARCHAR(50) NOT NULL REFERENCES SystèmeAnatomique(systèmeAnatomiqueNom)
                )""")

cursor.execute("""CREATE TABLE Medicament (
                DCI VARCHAR(50) PRIMARY KEY,
                medicamentNomCommercial VARCHAR(50) NOT NULL,
                conditionnement INT NOT NULL
                )""")

cursor.execute("""CREATE TABLE Employe (
                INAMI INT PRIMARY KEY,
                employeNom VARCHAR(50) NOT NULL,
                employeNum INT NOT NULL
                )""")

cursor.execute("""CREATE TABLE EmployeEmail (
                INAMI INT NOT NULL REFERENCES Employe(INAMI),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (INAMI, email)
                )""")

cursor.execute("CREATE TABLE Medecin LIKE Employe")
cursor.execute("ALTER TABLE Medecin ADD specialite VARCHAR(50) NOT NULL REFERENCES SystèmeAnatomique(systèmeAnatomiqueNom)")

cursor.execute("CREATE TABLE Pharmacien LIKE Employe")

cursor.execute("""CREATE TABLE Patient (
                patientId INT PRIMARY KEY,
                prenom VARCHAR(50) NOT NULL, 
                nom VARCHAR(50) NOT NULL,
                DateNaissance DATE NOT NULL,
                medecinDeReferenceINAMI INT NOT NULL REFERENCES Medecin(INAMI),
                pharmacienDeReferenceINAMI INT NOT NULL REFERENCES Pharmacien(INAMI)
                )""")

cursor.execute("""CREATE TABLE patientEmail (
                patientId INT NOT NULL REFERENCES Patient(patientId),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (patientId, email) 
                )""") #besoin de email ?

cursor.execute("""CREATE TABLE patientGSM (
                patientId INT NOT NULL REFERENCES Patient(patientId),
                numeroGSM INT NOT NULL,
                PRIMARY KEY (patientId, numeroGSM)
                )""") # besoin de numeroGSM ?

cursor.execute("""CREATE TABLE Dossier (
                patientId INT PRIMARY KEY REFERENCES Patient(patientId)
                )""")

cursor.execute("""CREATE TABLE DossierPathologie (
                patientId INT NOT NULL REFERENCES Dossier(patientId),
                pathologieNom VARCHAR(50) NOT NULL REFERENCES Pathologie(pathologieNom),
                dateDiagnostic  DATE NOT NULL,
                PRIMARY KEY (patientId, pathologieNom)
                )""")

cursor.execute("""CREATE TABLE Diagnostic (
                medecinINAMI INT NOT NULL REFERENCES Medecin(INAMI),
                patientId INT NOT NULL REFERENCES Dossier(patientId),
                pathologieNom VARCHAR(50) NOT NULL REFERENCES Pathologie(pathologieNom),
                dateDiagnostic DATE NOT NULL,
                PRIMARY KEY (medecinINAMI ,patientId, pathologieNom)
                )""")

cursor.execute("""CREATE TABLE Prescription  (
                patientId INT NOT NULL REFERENCES Dossier(patientId),
                DCI VARCHAR(50) NOT NULL REFERENCES Medicament(DCI),
                medecinINAMI INT NOT NULL REFERENCES Medecin(INAMI),
                Duree INT NOT NULL,
                PRIMARY KEY (medecinINAMI ,patientId, DCI)
                )""")

cursor.execute("""CREATE TABLE Traitement (
                patientId INT NOT NULL REFERENCES Dossier(patientId),
                DCI VARCHAR(50) NOT NULL REFERENCES Medicament(DCI),
                dateDébut DATE NOT NULL,
                medecinINAMI INT NOT NULL REFERENCES Medecin(INAMI),
                pharmacienINAMI INT NOT NULL REFERENCES Pharmacien(INAMI),
                Duree INT NOT NULL,
                PRIMARY KEY (patientId, DCI, dateDébut)
                )""")

cursor.execute("""CREATE TABLE Délivrance (
                pharmacienINAMI INT NOT NULL REFERENCES Pharmacien(INAMI),
                medecinINAMI INT NOT NULL REFERENCES Medecin(INAMI),
                patientId INT NOT NULL REFERENCES Patient(patient_id),
                DCI VARCHAR(50) NOT NULL REFERENCES Medicament(DCI),
                PRIMARY KEY (pharmacienINAMI, medecinINAMI, patientId, DCI)
                )""")

# Add data base
cursor.execute("INSERT INTO Pharmacien" )("INSERT INTO VALUES(%s,%s)",())
cursor.execute("INSERT INTO Medecin VALUES(%s,%s)",())
cursor.execute("INSERT INTO Patient VALUES(%s,%s)",())
cursor.execute("INSERT INTO Dossier VALUES(%s,%s)",()) 
cursor.execute("INSERT INTO Diagnostic VALUES(%s,%s)",()) 
cursor.execute("INSERT INTO Pescription VALUES(%s,%s)",()) 
cursor.execute("INSERT INTO Traitement VALUES(%s,%s)",())
cursor.execute("INSERT INTO Delivrance (pharmacienINAMI INT,medecinINAMI INT,patientId INT ,DCI VARCHAR(50))VALUES(%i,%i,%i,%s)",() ) 
cursor.execute("INSERT INTO PathologieVALUES(%s,%s)",())
cursor.execute("INSERT INTO DSystème AnatomiqueVALUES(%s,%s)",())


# Commit the changes and close the cursor and connection objects
cnx.commit()
cursor.close()
cnx.close()
