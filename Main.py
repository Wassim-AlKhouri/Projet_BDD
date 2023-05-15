import tkinter as tk
from tkinter import messagebox
import mysql.connector

class MyGUI():


    def __init__(self,cursor,connection):
        """Initializes the GUI"""

        self.cursor = cursor
        self.connection = connection

        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.title("Groupe AX")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.queriesmenu = tk.Menu(self.root, tearoff=0)
        for i in range(1,11):
            command = self.createQueryCommand(i)
            self.queriesmenu.add_command(label=f"Query {i}", command=command)
    
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label="Queries", menu=self.queriesmenu)
        self.root.config(menu=self.menubar)

        self.text = tk.Label(self.root, text="Connection", font=("Helvetica", 16), pady=20)
        self.text.pack()

        self.entryNISS = tk.Entry(self.root, width=30, justify="center")
        self.entryNISS.insert(0, "54723498984")
        self.entryNISS.bind("<FocusIn>", lambda event, arg="NISS": self.clear_default_entry(event, arg))
        self.entryNISS.pack(pady=10)

        self.button = tk.Button(self.root, text="Connect", width=20, command=self.connect)
        self.button.pack(pady=10)

        self.root.mainloop()


    def clear_default_entry(self, event, arg):
        """Clears the default text in the entry widget when clicked on"""
        if event.widget.get() == arg:
            event.widget.delete(0, tk.END)


    def on_closing(self):
        """Asks the user if he wants to quit the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    
    def createQueryCommand(self, i):
        return lambda: self.launch_query(i)


    def launch_query(self,number):
        """Launches the query"""

        query_data = {
            1: {"description": "La liste des noms commerciaux de médicaments correspondant à un nom en DCI, classés par ordre alphabétique et taille de conditionnement.", "entries": [{"label": "DCI", "default_value": "DCI"}]},
            2: {"description": "La liste des pathologies qui peuvent être prise en charge par un seul type de spécialistes", "entries": [{"label": "specialite", "default_value": "specialite"}]},
            3: {"description": "La spécialité de médecins pour laquelle les médecins prescrivent le plus de médicaments"},
            4: {"description": "Tous les utilisateurs ayant consommé un médicament spécifique (sous son nom commercial) après une date donnée, par exemple en cas de rappel de produit pour lot contaminé", "entries": [{"label": "NomCommercial", "default_value": "NomCommercial"}, {"label": "Date De Prescription (YYYY-MM-DD)", "default_value": "Date De Prescription (YYYY-MM-DD)"}]},
            5: {"description": "Tous les patients ayant été traités par un médicament (sous sa DCI) à une date antérieure mais qui ne le sont plus,pour vérifier qu'un patient suive bien un traitement chronique", "entries": [{"label": "DCI", "default_value": "DCI"}]},
            6: {"description": "La liste des médecins ayant prescrit des médicaments ne relevant pas de leur spécialité"},
            7: {"description": "Pour chaque décennie entre 1950 et 2020,(1950-59,1960-69,...),le médicament le plus consommé par des patients nés durant cette décennie"},
            8: {"description": "Quelle est la pathologie la plus diagnostiquée"},
            9: {"description": "Pour chaque patient,le nombre de médecin lui ayant prescrit un médicament ", "entries": [{"label": "NISS", "default_value": "NISS"}]},
            10: {"description": "La liste de médicament n'étant plus prescrit depuis une date spécifique", "entries": [{"label": "Date de prescription (YYYY-MM-DD)", "default_value": "Date de prescription (YYYY-MM-DD)"}]}
        }
        data = query_data[number]

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Query {number}")
        new_window.geometry("600x600")

        text = tk.Text(new_window, height=5, width=50,wrap="word")
        text.insert(tk.END, data["description"])
        text.configure(state="disabled")
        text.pack()
        
        entries = []
        for entry_data  in data.get("entries",[]):
            entry = tk.Entry(new_window, width=30, justify="center")
            entry.insert(0, entry_data.get("default_value", ""))
            entry.bind("<FocusIn>", lambda event, arg=entry_data["label"]: self.clear_default_entry(event, arg))
            entry.pack(pady=10)
            entries.append(entry)

        button = tk.Button(new_window, text="Launch", width=20, command=lambda: self.launch_quary(number,self.cursor,[entry.get() for entry in entries]))
        button.pack(pady=10)


    def launch_quary(self,number,cursor,args):
        """
        Launches the query where number is the number of the query
        and args are the arguments of the query.
        returns the result
        """
        with open(f'query_{number}.sql', 'r') as f:
            sql = f.read()
        named_args = {f'placeholder{i+1}': arg for i, arg in enumerate(args)}
        sql = sql.format(**named_args)
        cursor.execute(sql)
        results = cursor.fetchall()

        result_window = tk.Toplevel(self.root)
        result_window.title(f"Query {number} result")
        result_window.geometry("600x600")
        
        listbox = tk.Listbox(result_window,justify="center")
        for result in results:
            listbox.insert(tk.END, result)
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')


    def connect(self):
        """Connects to the database"""
        self.NISS = self.entryNISS.get()

        infoPatient, infoMedecin, infoPharmacien = self.getPatientInfo()
        if(infoPatient == None or infoMedecin == None or infoPharmacien == None):
            messagebox.showerror("Error", "Les informations n'ont pas été trouvées")
            return

        self.root.withdraw()

        self.clientWindow = tk.Toplevel(self.root)
        self.clientWindow.title(f"Client {infoPatient[0]}")
        self.clientWindow.geometry("500x500")
        self.clientWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.clientInfo = tk.Text(self.clientWindow, height=7, width=50,wrap="word")
        self.clientInfo.pack()

        self.updateClientInfo(infoPatient, infoMedecin, infoPharmacien)
        
        buttonChangerMedecin = tk.Button(self.clientWindow, text="Changer de medecin", width=30, command = lambda:self.changeMedecinPharmacien("medecin"))
        buttonChangerMedecin.pack(pady=10)

        buttonChangerPharmacien = tk.Button(self.clientWindow, text="Changer de pharmacien", width=30, command = lambda:self.changeMedecinPharmacien("pharmacien"))
        buttonChangerPharmacien.pack(pady=10)

        buttonConsulterInfoMed = tk.Button(self.clientWindow, text="Consulter les informations médicales", width=30, command = self.consulterInfoMed)
        buttonConsulterInfoMed.pack(pady=10)

        buttonConsulterTraitement = tk.Button(self.clientWindow, text="Consulter les traitements", width=30, command = self.consulterTraitement)
        buttonConsulterTraitement.pack(pady=10)

        buttonReturn = tk.Button(self.clientWindow, text="Retour", width=30, command = lambda: self.returnToParentWindow(self.clientWindow,self.root))
        buttonReturn.place(relx=0.5, rely=0.9, anchor='center')

    
    def refrechClientInfo(self):
        """Refreshes the info of the client"""
        infoPatient, infoMedecin, infoPharmacien = self.getPatientInfo()
        self.updateClientInfo(infoPatient, infoMedecin, infoPharmacien)


    def updateClientInfo(self, infoPatient, infoMedecin, infoPharmacien):
        """Updates the info of the client"""
        self.clientInfo.configure(state="normal")

        self.clientInfo.delete("1.0", tk.END)

        self.clientInfo.insert(tk.END,"Nom : " + infoPatient[0] + "\n")
        self.clientInfo.insert(tk.END,"Prenom : " + infoPatient[1] + "\n")
        
        self.clientInfo.insert(tk.END,"Medecin de reference :" + "\n")
        self.clientInfo.insert(tk.END," - Nom : " + infoMedecin[0] + "\n")
        self.clientInfo.insert(tk.END," - Specialite : " + infoMedecin[1] + "\n")
        
        self.clientInfo.insert(tk.END,"Pharmacien de reference :" + "\n")
        self.clientInfo.insert(tk.END," - Nom : " + infoPharmacien[0] + "\n")

        self.clientInfo.configure(state="disabled")


    def getPatientInfo(self):
        """Gets the info of the patient from the database"""
        self.cursor.execute(f"""SELECT nom,prenom,medecinDeReferenceINAMI,pharmacienDeReferenceINAMI 
                                FROM Patient 
                                WHERE NISS ={self.NISS}"""
                           )
        infoPatient = self.cursor.fetchone()

        self.medecinDeReferenceINAMI = infoPatient[2]
        self.pharmacienDeReferenceINAMI = infoPatient[3]

        self.cursor.execute(f"""SELECT employeNom,specialite 
                                FROM Medecin 
                                WHERE INAMI ={self.medecinDeReferenceINAMI}"""
                           )
        infoMedecin = self.cursor.fetchone()
        
        self.cursor.execute(f"""SELECT employeNom 
                                FROM Pharmacien 
                                WHERE INAMI ={self.pharmacienDeReferenceINAMI}"""
                           )
        infoPharmacien = self.cursor.fetchone()
        
        return infoPatient,infoMedecin,infoPharmacien


    def changeMedecinPharmacien(self,type):
        """Opens a window to change the medecin or the pharmacien"""
        info = {
            "medecin" : "INAMI,employeNom,specialite",
            "pharmacien" : "INAMI,employeNom"
        }
        self.cursor.execute(f"""SELECT {info[type]}
                                FROM {type.capitalize()}
                                WHERE INAMI !={self.medecinDeReferenceINAMI}"""
                            )
        infoEmploye = self.cursor.fetchall()

        self.clientWindow.withdraw()
        self.changeWindow = tk.Toplevel(self.clientWindow)
        self.changeWindow.title(f"Changer de {type}")
        self.changeWindow.geometry("500x500")
        self.changeWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        label = tk.Label(self.changeWindow, text=f"Choisissez un {type} :")
        label.pack(pady=10)

        listbox = tk.Listbox(self.changeWindow,justify="center")
        for medecin in infoEmploye:
            listbox.insert(tk.END, medecin)
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')

        button = tk.Button(self.changeWindow, text="Changer", width=20, command=lambda: self.changeMedecinPharmacienQuary(listbox.get(tk.ACTIVE),type))
        button.pack(pady=10)

        buttonReturn = tk.Button(self.changeWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.changeWindow,self.clientWindow))
        buttonReturn.pack(pady=10)

    
    def changeMedecinPharmacienQuary(self,employe,type):
        """Changes the medecin or the pharmacien in the database"""
        self.cursor.execute(f"""UPDATE Patient
                                SET {type}DeReferenceINAMI = {employe[0]}
                                WHERE NISS = {self.NISS}"""
                            )
        if(type == "medecin"):
            self.medecinDeReferenceINAMI = employe[0]
        else:
            self.pharmacienDeReferenceINAMI = employe[0]
        self.connection.commit()
        self.changeWindow.destroy()
        self.refrechClientInfo()
        self.clientWindow.deiconify()
    

    def consulterInfoMed(self):
        """Opens a window to consult the medical information of the client"""
        pass


    def consulterTraitement(self):
        """Opens a window to consult the treatments of the client"""
        self.cursor.execute(f"""SELECT *
                                FROM DossierPatient
                                WHERE NISS = {self.NISS}
                                ORDER BY datePrescription DESC"""
                            )
        infoDossier = self.cursor.fetchall()
        
        self.clientWindow.withdraw()
        self.traitementWindow = tk.Toplevel(self.clientWindow)
        self.traitementWindow.title("Traitements")
        self.traitementWindow.geometry("500x500")
        self.traitementWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        label = tk.Label(self.traitementWindow, text="Traitements :")
        label.pack(pady=10)

        text = tk.Text(self.traitementWindow, height=20, width=50)
        text.pack(pady=10)
        for traitement in infoDossier:
            text.insert(tk.END, f"{traitement[7]}, {traitement[5]} : \n")
            text.insert(tk.END, f"  - Medicament DCI : {traitement[6]} \n")
            text.insert(tk.END, f"  - Medecin : {traitement[1]} \n")
            text.insert(tk.END, f"  - Pharmacien : {traitement[3]} \n")
            text.insert(tk.END, f"  - Durée : {traitement[9]} \n")
            text.insert(tk.END, f"  - Date de vente : {traitement[8]} \n")
        text.configure(state="disabled")

        buttonReturn = tk.Button(self.traitementWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.traitementWindow,self.clientWindow))
        buttonReturn.pack(pady=10)


    def returnToParentWindow(self,subwindow,root):
        """Returns to the parent window"""
        subwindow.destroy()
        root.deiconify()


if __name__ == '__main__':
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost',
        database='groupAX_DB'
    )
    cursor = cnx.cursor()
    myGUI = MyGUI(cursor, cnx)

