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

cursor.execute("""CREATE TABLE anatomic_system (
                anatomic_system_name VARCHAR(50) PRIMARY KEY
                )""")

cursor.execute("""CREATE TABLE disease (
                disease_name VARCHAR(50) PRIMARY KEY,
                anatomic_system_name VARCHAR(50) NOT NULL REFERENCES anatomic_system(anatomic_system_name)
                )""")

cursor.execute("""CREATE TABLE medecin (
                DCI VARCHAR(50) PRIMARY KEY,
                commercial_name VARCHAR(50) NOT NULL,
                packaging INT NOT NULL
                )""")

cursor.execute("""CREATE TABLE employ (
                INAMI INT PRIMARY KEY,
                fristnam VARCHAR(50) NOT NULL,
                lastname VARCHAR(50) NOT NULL,
                phone_number INT NOT NULL
                )""")

cursor.execute("""CREATE TABLE employEmail (
                INAMI INT NOT NULL REFERENCES employ(INAMI),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (INAMI, email)
                )""")

cursor.execute("CREATE TABLE doctor LIKE employ")
cursor.execute("ALTER TABLE doctor ADD speciality VARCHAR(50) NOT NULL REFERENCES anatomic_system(anatomic_system_name)")

cursor.execute("CREATE TABLE pharmacist LIKE employ")

cursor.execute("""CREATE TABLE delivery (
                pharmacist_INAMI INT NOT NULL REFERENCES pharmacist(INAMI),
                doctor_INAMI INT NOT NULL REFERENCES doctor(INAMI),
                patient_id INT NOT NULL REFERENCES patient(patient_id),
                DCI VARCHAR(50) NOT NULL REFERENCES medecin(DCI),
                PRIMARY KEY (pharmacist_INAMI, doctor_INAMI, patient_id, DCI)
                )""")

cursor.execute("""CREATE TABLE patient (
                patient_id INT PRIMARY KEY,
                fristnam VARCHAR(50) NOT NULL, 
                lastname VARCHAR(50) NOT NULL,
                birthdate DATE NOT NULL,
                refernce_doctor_INAMI INT NOT NULL REFERENCES doctor(INAMI),
                refernce_pharmacist_INAMI INT NOT NULL REFERENCES pharmacist(INAMI)
                )""")

cursor.execute("""CREATE TABLE patientEmail (
                patient_id INT NOT NULL REFERENCES patient(patient_id),
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (patient_id, email) 
                )""") #besoin de email ?

cursor.execute("""CREATE TABLE patientPhone (
                patient_id INT NOT NULL REFERENCES patient(patient_id),
                phone_number INT NOT NULL,
                PRIMARY KEY (patient_id, phone_number)
                )""") # besoin de phone_number ?

cursor.execute("""CREATE TABLE patient_file (
                patient_id INT PRIMARY KEY REFERENCES patient(patient_id)
                )""")

cursor.execute("""CREATE TABLE patient_file_disease (
                patient_id INT NOT NULL REFERENCES patient_file(patient_id),
                disease_name VARCHAR(50) NOT NULL REFERENCES disease(disease_name),
                diagnosis_date DATE NOT NULL,
                PRIMARY KEY (patient_id, disease_name)
                )""")

cursor.execute("""CREATE TABLE diagnosis (
                doctor_INAMI INT NOT NULL REFERENCES doctor(INAMI),
                patient_id INT NOT NULL REFERENCES patient_file(patient_id),
                disease_name VARCHAR(50) NOT NULL REFERENCES disease(disease_name),
                diagnosis_date DATE NOT NULL,
                PRIMARY KEY (doctor_INAMI ,patient_id, disease_name)
                )""")

cursor.execute("""CREATE TABLE prescription (
                patient_id INT NOT NULL REFERENCES patient_file(patient_id),
                DCI VARCHAR(50) NOT NULL REFERENCES medecin(DCI),
                doctor_INAMI INT NOT NULL REFERENCES doctor(INAMI),
                duration INT NOT NULL,
                PRIMARY KEY (doctor_INAMI ,patient_id, DCI)
                )""")

cursor.execute("""CREATE TABLE treatment (
                patient_id INT NOT NULL REFERENCES patient_file(patient_id),
                DCI VARCHAR(50) NOT NULL REFERENCES medecin(DCI),
                starting_date DATE NOT NULL,
                doctor_INAMI INT NOT NULL REFERENCES doctor(INAMI),
                pharmacist_INAMI INT NOT NULL REFERENCES pharmacist(INAMI),
                duration INT NOT NULL,
                PRIMARY KEY (patient_id, DCI, starting_date)
                )""")

# Commit the changes and close the cursor and connection objects
cnx.commit()
cursor.close()
cnx.close()
