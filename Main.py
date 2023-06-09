import tkinter as tk
from tkinter import IntVar, messagebox
import mysql.connector
from datetime import datetime


class MyGUI():


    def __init__(self,cursor,connection):
        """Initializes the GUI"""
        ### INTI cursor and connection ###
        self.cursor = cursor
        self.connection = connection
        ### Create the root window ###
        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.title("Groupe AX")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the menu with the queries ###
        self.queriesmenu = tk.Menu(self.root, tearoff=0)
        for i in range(1,11):
            command = self.createQueryCommand(i)
            self.queriesmenu.add_command(label=f"Query {i}", command=command)
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label="Queries", menu=self.queriesmenu)
        self.root.config(menu=self.menubar)
        ### Create the connection frame ###
        ## Connection text ##
        self.text = tk.Label(self.root, text="Connection", font=("Helvetica", 16), pady=20)
        self.text.pack()
        ## Entry ##
        self.entryNISS = tk.Entry(self.root, width=30, justify="center")
        self.entryNISS.insert(0, "NISS")
        # client test NISS: 393834744538
        self.entryNISS.bind("<FocusIn>", lambda event, arg="NISS": self.clear_default_entry(event, arg))
        self.entryNISS.pack(pady=10)
        ## Button ##
        self.button = tk.Button(self.root, text="Connect", width=20, command=self.connect)
        self.button.pack(pady=10)
        ### Run the main loop ###
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
            1: {"description": "La liste des noms commerciaux de médicaments correspondant à un nom en DCI, classés par ordre alphabétique et taille de conditionnement.", "entries": ["DCI"]},
            2: {"description": "La liste des pathologies qui peuvent être prise en charge par un seul type de spécialistes"},
            3: {"description": "La spécialité de médecins pour laquelle les médecins prescrivent le plus de médicaments"},
            4: {"description": "Tous les utilisateurs ayant consommé un médicament spécifique (sous son nom commercial) après une date donnée, par exemple en cas de rappel de produit pour lot contaminé", "entries": ["NomCommercial","Date De Prescription (YYYY-MM-DD)"]},
            5: {"description": "Tous les patients ayant été traités par un médicament (sous sa DCI) à une date antérieure mais qui ne le sont plus,pour vérifier qu'un patient suive bien un traitement chronique", "entries": ["DCI"]},
            6: {"description": "La liste des médecins ayant prescrit des médicaments ne relevant pas de leur spécialité"},
            7: {"description": "Pour chaque décennie entre 1950 et 2020,(1950-59,1960-69,...),le médicament le plus consommé par des patients nés durant cette décennie"},
            8: {"description": "Quelle est la pathologie la plus diagnostiquée"},
            9: {"description": "Pour chaque patient,le nombre de médecin lui ayant prescrit un médicament "},
            10: {"description": "La liste de médicament n'étant plus prescrit depuis une date spécifique", "entries": ["Date de prescription (YYYY-MM-DD)"]}
        }
        data = query_data[number]
        ### Create the new window ###
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Query {number}")
        new_window.geometry("600x600")
        ### Create the widgets ###
        ## Description ##
        text = tk.Text(new_window, height=5, width=50,wrap="word")
        text.insert(tk.END, data["description"])
        text.configure(state="disabled")
        text.pack()
        ## Entries ##
        entries = []
        for entry_data  in data.get("entries",[]):
            entry = tk.Entry(new_window, width=35, justify="center")
            entry.insert(0, entry_data)
            entry.bind("<FocusIn>", lambda event, arg=entry_data: self.clear_default_entry(event, arg))
            entry.pack(pady=10)
            entries.append(entry)
        ## Button ##
        button = tk.Button(new_window, text="Launch", width=20, command=lambda: self.executeQuary(number,self.cursor,[entry.get() for entry in entries]))
        button.pack(pady=10)


    def executeQuary(self,number,cursor,args):
        """Executes the query number with the given arguments."""
        ### Get the query and execute it ###
        with open(f'queries/query_{number}.sql', 'r') as f:
            sql = f.read()
        if len(args) > 0:
            named_args = {f'placeholder{i+1}': arg for i, arg in enumerate(args)}
            sql = sql.format(**named_args)
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == 1525:
                messagebox.showerror("Error", "Invalid date value\nFormat: YYYY-MM-DD")
                return
            else:
                print(err)
                exit(1)
        results = cursor.fetchall()
        ### Create the new window ###
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Query {number} result")
        result_window.geometry("600x600")
        ### Create the list ###
        listbox = tk.Listbox(result_window,justify="center")
        for result in results:
            listbox.insert(tk.END, result)
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')


    def connect(self):
        """Connects to the database and creates the main window"""
        self.NISS = self.entryNISS.get()
        ### Get the patient info from the database ###
        infoPatient, infoMedecin, infoPharmacien = self.getPatientInfo()
        if(infoPatient == None or infoMedecin == None or infoPharmacien == None):
            messagebox.showerror("Error", "Les informations n'ont pas été trouvées")
            print("Patient",infoPatient)
            print("Medecin",infoMedecin)
            print("Pharmacien",infoPharmacien)
            return
        self.root.withdraw()
        ### Create the new window ###
        self.clientWindow = tk.Toplevel(self.root)
        self.clientWindow.title(f"Client {infoPatient[0]}")
        self.clientWindow.geometry("500x600")
        self.clientWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## Patient info ##
        self.clientInfo = tk.Text(self.clientWindow, height=7, width=50,wrap="word")
        self.clientInfo.pack()
        self.updateClientInfo(infoPatient, infoMedecin, infoPharmacien)
        ## Buttons ##
        # Change Medecin #
        buttonChangerMedecin = tk.Button(self.clientWindow, text="Changer de medecin", width=30, command = lambda:self.changeMedecinPharmacien("medecin"))
        buttonChangerMedecin.pack(pady=10)
        # Chercher Expert #
        buttonChercherExpert = tk.Button(self.clientWindow, text="Chercher un expert", width=30, command = self.chercherExpert)
        buttonChercherExpert.pack(pady=10)
        # Change Pharmacien #
        buttonChangerPharmacien = tk.Button(self.clientWindow, text="Changer de pharmacien", width=30, command = lambda:self.changeMedecinPharmacien("pharmacien"))
        buttonChangerPharmacien.pack(pady=10)
        # Consult info #
        buttonConsulterInfoMed = tk.Button(self.clientWindow, text="Consulter les informations du client", width=30, command = self.consulterInfo)
        buttonConsulterInfoMed.pack(pady=10)
        # Consult traitement #
        buttonConsulterTraitement = tk.Button(self.clientWindow, text="Consulter les traitements", width=30, command = self.consulterTraitement)
        buttonConsulterTraitement.pack(pady=10)
        # Consult diagnostic #
        buttonConsulterDiagostic = tk.Button(self.clientWindow, text="Consulter les diagnostics", width=30, command = self.consulterDiagnostic)
        buttonConsulterDiagostic.pack(pady=10)
        # Faceted search#
        buttonFactedSearch = tk.Button(self.clientWindow, text="Recherche à facettes", width=30, command = lambda : self.facetedSearch(0,self.clientWindow))
        buttonFactedSearch.pack(pady=10)
        # Return #
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
        self.clientInfo.insert(tk.END,"Nom : " + infoPatient[5] + "\n")
        self.clientInfo.insert(tk.END,"Prenom : " + infoPatient[6] + "\n")
        self.clientInfo.insert(tk.END,"Medecin de reference :" + "\n")
        self.clientInfo.insert(tk.END," - Nom : " + infoMedecin[0] + "\n")
        self.clientInfo.insert(tk.END," - Specialite : " + infoMedecin[1] + "\n")
        self.clientInfo.insert(tk.END,"Pharmacien de reference :" + "\n")
        self.clientInfo.insert(tk.END," - Nom : " + infoPharmacien[0] + "\n")
        self.clientInfo.configure(state="disabled")


    def getPatientInfo(self):
        """Gets the info of the patient from the database"""
        # Get the info of the patient #
        self.cursor.execute(f"""SELECT * 
                                FROM Patient 
                                WHERE NISS ={self.NISS}"""
                           )
        infoPatient = self.cursor.fetchone()
        if(infoPatient == None):
            return None,None,None
        
        self.medecinDeReferenceINAMI = infoPatient[3]
        self.pharmacienDeReferenceINAMI = infoPatient[4]
        # Get the info of the medecin #
        self.cursor.execute(f"""SELECT employeNom,specialite 
                                FROM Medecin 
                                WHERE INAMI ={self.medecinDeReferenceINAMI}"""
                           )
        infoMedecin = self.cursor.fetchone()
        # Get the info of the pharmacien #
        self.cursor.execute(f"""SELECT employeNom 
                                FROM Pharmacien 
                                WHERE INAMI ={self.pharmacienDeReferenceINAMI}"""
                           )
        infoPharmacien = self.cursor.fetchone()
        return infoPatient,infoMedecin,infoPharmacien
    

    def changeMedecinPharmacien(self,type):
        """Opens a window to change the medecin or the pharmacien"""
        ### Get the info of the medecin/pharmacien ###
        info = {
            "medecin" : "INAMI,employeNom,specialite",
            "pharmacien" : "INAMI,employeNom"
        }
        self.cursor.execute(f"""SELECT {info[type]}
                                FROM {type.capitalize()}
                                WHERE INAMI !={self.medecinDeReferenceINAMI}"""
                            )
        infoEmploye = self.cursor.fetchall()
        ### Create the new window ###
        self.clientWindow.withdraw()
        self.changeWindow = tk.Toplevel(self.clientWindow)
        self.changeWindow.title(f"Changer de {type}")
        self.changeWindow.geometry("500x500")
        self.changeWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## text ##
        label = tk.Label(self.changeWindow, text=f"Choisissez un {type} :")
        label.pack(pady=10)
        ## listbox ##
        listbox = tk.Listbox(self.changeWindow,justify="center")
        for employe in infoEmploye:
            if (type == "medecin"):
                listbox.insert(tk.END, (employe[0],employe[1],employe[2].replace(" ","_")))
            else:
                listbox.insert(tk.END, (employe[0],employe[1]))
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')
        ## buttons ##
        # Change button #
        button = tk.Button(self.changeWindow, text="Changer", width=20, command=lambda: self.changeMedecinPharmacienQuary(listbox.get(tk.ACTIVE),type))
        button.pack(pady=10)
        # Return button #
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

    def facetedSearch(self, type, lastwindow):
        """Opens a window that allows a client to access public information in the database and apply different filters"""
        ### Create the new window ###
        lastwindow.withdraw()
        self.facetWindow = tk.Toplevel(self.clientWindow)
        self.facetWindow.title("Recherche à facettes")
        self.facetWindow.geometry("500x500")
        self.facetWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## variable ##
        var = IntVar()
        search  = {
            0 : ('Médecin', 'Médicament', 'Pathologie'),
            1 : ('Spécialité', 'Ordre alphabétique'),
            2 : ('DCI','Système anatomique'),
            3 : ('Spécialité traitant la pathologie', 'Ordre alphabétique')
        }
        ## text ##
        label = tk.Label(self.facetWindow, text="Sélectionnez des fitres de recherche : ")
        label.pack(pady=10)
        ## RadioButton ##
        for i in range(len(search[type])):
            option = tk.Radiobutton(self.facetWindow,text=search[type][i],variable=var,value=(i+1))
            option.pack(pady=10)
        ## Button ##
        # Select search filters #
        if type == 0:
            button = tk.Button(self.facetWindow,text='Sélectionner', width=20, command=lambda: self.facetedSearch(var.get(),self.facetWindow))
            button.pack(pady=10)
        else : 
            button = tk.Button(self.facetWindow,text='Sélectionner', width=20, command=lambda: self.facetedSearch2(type-1,var.get()-1,self.facetWindow))
            button.pack(pady=10)
        # Return button #
        buttonReturn = tk.Button(self.facetWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.facetWindow,self.clientWindow))
        buttonReturn.pack(pady=10)


    def facetedSearch2(self, variable1, variable2, lastwindow):
        ### Get Info ###
        info = []
        if variable1 == 0:
            if variable2 == 0:
                self.cursor.execute("""SELECT DISTINCT specialite
                                    FROM Medecin""")
                info = self.cursor.fetchall()
            else:
                info = {'ASC', 'DESC'}
        elif variable1 == 1:
            if variable2 == 0:
                self.cursor.execute("""SELECT DISTINCT DCI
                                    FROM Medicament""")
                info = self.cursor.fetchall()
            else:
                self.cursor.execute("""SELECT DISTINCT systemeAnatomiqueNom
                                    FROM Medicament""")
                info = self.cursor.fetchall()
        else:
            if variable2 == 0:
                self.cursor.execute("""SELECT DISTINCT specialiteNom
                                    FROM Pathologie
                                    """)
                info = self.cursor.fetchall()
            else:
                info = {'ASC', 'DESC'}

        ### Create the new window ###
        lastwindow.withdraw()
        self.facetWindow2 = tk.Toplevel(self.clientWindow)
        self.facetWindow2.title("Recherche à facettes")
        self.facetWindow2.geometry("500x500")
        self.facetWindow2.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## Listbox ##
        listbox = tk.Listbox(self.facetWindow2, justify="center")
        for i in info:
            listbox.insert(tk.END, i)
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')
        button = tk.Button(self.facetWindow2,text='Sélectionner', width=20, command = lambda: self.facetedSearchQueries(variable1,variable2,listbox.get(tk.ACTIVE),listbox,button))
        button.pack(pady=10)
        ## Button ##
        # Return button #
        buttonReturn = tk.Button(self.facetWindow2, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.facetWindow2,self.facetWindow))
        buttonReturn.pack(pady=10)
        
    def facetedSearchQueries(self,variable1,variable2,entry,listbox,button):
        ## Button ##
        button.destroy()
        query = [[f"""SELECT m.employeNom, m.INAMI FROM Medecin m WHERE m.Specialite = '{entry[0]}'""",f"""SELECT m.employeNom, m.INAMI FROM Medecin m ORDER BY m.employeNom {entry}"""],
                 [f"""SELECT DISTINCT m.medicamentNomCommercial FROM Medicament m WHERE m.DCI = '{entry[0]}'""",f"""SELECT DISTINCT m.medicamentNomCommercial FROM Medicament m WHERE m.systemeAnatomiqueNom = '{entry[0]}'"""],
                 [f"""SELECT p.pathologieNom FROM Pathologie p WHERE p.specialiteNom = '{entry[0]}'""",f"""SELECT p.pathologieNom FROM Pathologie p ORDER BY p.pathologieNom {entry}"""]]
        self.cursor.execute(query[variable1][variable2])
        searchResult = self.cursor.fetchall()
        if(searchResult ==[]):
            messagebox.showerror("Erreur","Aucun résultat trouvé")
        else:
            listbox.delete(0,tk.END)
            for result in searchResult:
                listbox.insert(tk.END, result)  

    
    def chercherExpert(self) : 
        """Opens a window to search for an expert"""
        ### Create the new window ###
        self.clientWindow.withdraw()
        self.changeWindow = tk.Toplevel(self.clientWindow)
        self.changeWindow.title("Chercher un expert")
        self.changeWindow.geometry("500x500")
        self.changeWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## text ##
        label = tk.Label(self.changeWindow, text="Choisissez une pathologie :")
        label.pack(pady=10)
        ## Entry ##
        entry = tk.Entry(self.changeWindow, width=20)
        entry.pack(pady=10)
        ## listbox ##
        listbox = tk.Listbox(self.changeWindow,justify="center")
        listbox.pack(expand=True, fill='both', padx=10, pady=10, anchor='center')
        ## buttons ##
        # Search button #
        button = tk.Button(self.changeWindow, text="Chercher", width=20, command=lambda: self.searchExpertQuary(entry.get(),listbox))
        button.pack(pady=10)
        # Change Doctor button #
        button = tk.Button(self.changeWindow, text="Changer", width=20, command=lambda: self.changeMedecinPharmacienQuary(listbox.get(tk.ACTIVE),"medecin"))
        button.pack(pady=10)
        # Return button #
        buttonReturn = tk.Button(self.changeWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.changeWindow,self.clientWindow))
        buttonReturn.pack(pady=10)
        

    def searchExpertQuary(self,pathologie,listbox):
        """Search for an expert in the database"""
        ### Get the list of the experts ###
        self.cursor.execute(f"""SELECT m.INAMI, m.employeNOM, COUNT(*)
                                FROM Medecin m
                                JOIN DossierPatient dp ON dp.medecinINAMI = m.INAMI
                                JOIN Diagnostic d ON d.NISS = dp.NISS
                                WHERE d.pathologieNom = '{pathologie}'
                                GROUP BY dp.medecinINAMI
                                ORDER BY COUNT(*) DESC, m.employeNOM ASC
                                """)
        infoMedecin = self.cursor.fetchall()
        ### Inject the info in the listbox ###
        if (infoMedecin == []):
            messagebox.showerror("Erreur", "Aucun expert trouvé")
        else:
            listbox.delete(0, tk.END)
            for medecin in infoMedecin:
                listbox.insert(tk.END, medecin)
    

    def consulterInfo(self):
        """Opens a window to consult the informations of the client"""
        ### Get the info of the client ###
        infoPatient,_,_ = self.getPatientInfo()
        ## Get Email ##
        self.cursor.execute(f"""SELECT *
                                FROM PatientEmail
                                WHERE NISS = {self.NISS}"""
                            )
        infoPatientEmail = self.cursor.fetchall()
        Email = infoPatientEmail[0][1] if infoPatientEmail[0][1] != "None" else "Pas d'email"
        ## Get GSM ##
        self.cursor.execute(f"""SELECT *
                                FROM PatientGSM
                                WHERE NISS = {self.NISS}"""
                            )
        infoPatientGSM = self.cursor.fetchall()
        GSM = infoPatientGSM[0][1] if infoPatientGSM[0][1] != "None" else "Pas de GSM"
        ### Create the new window ###
        self.clientWindow.withdraw()
        self.infoWindow = tk.Toplevel(self.clientWindow)
        self.infoWindow.title("Informations")
        self.infoWindow.geometry("500x500")
        self.infoWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## texts ##
        # Title #
        label = tk.Label(self.infoWindow, text="Informations :")
        label.pack(pady=10)
        # Info #
        text = tk.Text(self.infoWindow, height=6, width=55)
        text.pack(pady=10)
        Nom,Prenom,DateNaissance,Genre = infoPatient[5],infoPatient[6],infoPatient[1],infoPatient[2]
        text.insert(tk.END,f"Nom : {Nom}\n")
        text.insert(tk.END,f"Prenom : {Prenom}\n")
        text.insert(tk.END,f"Date de naissance : {DateNaissance}\n")
        text.insert(tk.END,f"Genre : {Genre}\n")
        text.insert(tk.END,f"Telephone : {GSM}\n")
        text.insert(tk.END,f"Email : {Email}\n")
        text.config(state="disabled")
        ## Buttons ##
        # Change button #
        buttonChange = tk.Button(self.infoWindow, text="Changer", width=20, command = lambda: self.changeInfo([Nom,Prenom,DateNaissance,Genre,GSM,Email]))
        buttonChange.pack(pady=10)
        # Return button #
        buttonReturn = tk.Button(self.infoWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.infoWindow,self.clientWindow))
        buttonReturn.pack(pady=10)
        

    def changeInfo(self,info):
        """Opens a window to change the informations of the client"""
        ### Create the new window ###
        self.infoWindow.withdraw()
        self.changeInfoWindow = tk.Toplevel(self.infoWindow)
        self.changeInfoWindow.title("Changer les informations")
        self.changeInfoWindow.geometry("500x500")
        self.changeInfoWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## Entries ##
        entries = []
        for i in info:
            entry = tk.Entry(self.changeInfoWindow, width=40, justify="center")
            entry.insert(0,i)
            entry.pack(pady=10)
            entries.append(entry)
        ## Buttons ##
        # Change button #
        buttonChange = tk.Button(self.changeInfoWindow, text="Changer", width=20, command = lambda: self.changeInfoQuary(entries))
        buttonChange.pack(pady=10)
        # Return button #
        buttonReturn = tk.Button(self.changeInfoWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.changeInfoWindow,self.infoWindow))
        buttonReturn.pack(pady=10)
        

    def changeInfoQuary(self,entries):
        """Changes the informations of the client in the database"""
        ### Get the info ###
        info = []
        for entry in entries:
            info.append(entry.get())
        ### Change the info in the database ###
        ## Tests ##
        # Date #
        if self.isDateSqlFormat(info[2]) == False:
            messagebox.showerror("Error", "La date n'est pas au bon format\nFormat : YYYY-MM-DD")
            return
        # GSM #
        if info[4] != "Pas de GSM" and info[4] != "":
            if self.isGSMFormat(info[4]) == False:
                messagebox.showerror("Error", "Le numero de telephone n'est pas au bon format\nFormat : 04XX XX XX XX")
                return
        # Email #
        if info[5] != "Pas d'email" and info[5] != "":
            if self.isEmailFormat(info[5]) == False:
                messagebox.showerror("Error", "L'email n'est pas au bon format\nFormat : XX@XX.XX\n and length < 50")
                return
        ## Update Patient ##
        self.cursor.execute(f"""UPDATE Patient
                                SET nom = '{info[0]}',
                                    prenom = '{info[1]}',
                                    dateNaissance = '{info[2]}',
                                    genre = '{info[3]}'
                                WHERE NISS = {self.NISS}"""
                            )
        ## Update PatientGSM ##
        if (info[4] != "Pas de GSM" and info[4] != ""):
            GSM = info[4]
        else :
            GSM = "None"
        self.cursor.execute(f"""UPDATE PatientGSM
                                SET numeroGSM = '{GSM}'
                                WHERE NISS = {self.NISS}"""
                            )
        ## Update PatientEmail ##
        if (info[5] != "Pas d'email" and info[5] != ""):
            email = info[5]
        else :
            email = "None"
        self.cursor.execute(f"""UPDATE PatientEmail
                                SET email = '{email}'
                                WHERE NISS = {self.NISS}"""
                            )
        ### Commit the changes ###
        self.connection.commit()
        self.changeInfoWindow.destroy()
        self.refrechClientInfo()
        self.infoWindow.destroy()
        self.clientWindow.deiconify()


    def consulterTraitement(self):
        """Opens a window to consult the treatments of the client"""
        ### Get the info of the client ###
        ## Active Treatements ##
        self.cursor.execute(f"""SELECT *,
                                DATE_ADD(datePrescription, INTERVAL dureeTraitement DAY) AS dateFinTraitement
                                FROM DossierPatient
                                WHERE NISS = {self.NISS} 
                                    AND DATE_ADD(datePrescription, INTERVAL dureeTraitement DAY) >= CURRENT_DATE()
                                ORDER BY datePrescription DESC
                                """)
        ActiveTreatements = self.cursor.fetchall()
        ## Past Treatements ##
        self.cursor.execute(f"""SELECT *,
                                DATE_ADD(datePrescription, INTERVAL dureeTraitement DAY) AS dateFinTraitement
                            FROM DossierPatient
                            WHERE NISS = {self.NISS} 
                                AND DATE_ADD(datePrescription, INTERVAL dureeTraitement DAY) < CURRENT_DATE()
                            ORDER BY datePrescription DESC
                            """)
        PastTreatements = self.cursor.fetchall()
        ## Conflicting Treatements ##
        self.cursor.execute(f"""SELECT DCI
                                FROM DossierPatient
                                WHERE NISS = {self.NISS} 
                                    AND DATE_ADD(datePrescription, INTERVAL dureeTraitement DAY) >= CURRENT_DATE()
                                GROUP BY DCI
                                HAVING COUNT(*) > 1
                                """)
        ConflictingTreatements = self.cursor.fetchall()
        ### Create the new window ###
        self.clientWindow.withdraw()
        self.traitementWindow = tk.Toplevel(self.clientWindow)
        self.traitementWindow.title("Traitements")
        self.traitementWindow.geometry("500x500")
        self.traitementWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## Active ##
        # Title #
        label = tk.Label(self.traitementWindow, text="Traitements actives :")
        label.pack(pady=10)
        # Info #
        text = tk.Text(self.traitementWindow, height=10, width=55)
        text.pack(pady=10)
        for traitement in ActiveTreatements:
            text.insert(tk.END, f"{traitement[7]}, {traitement[5]} : \n")
            text.insert(tk.END, f"  - Medicament DCI : {traitement[6]} \n")
            text.insert(tk.END, f"  - Medecin : {traitement[1]} \n")
            text.insert(tk.END, f"  - Pharmacien : {traitement[3]} \n")
            text.insert(tk.END, f"  - Durée : {traitement[9]} \n")
            text.insert(tk.END, f"  - Date de vente : {traitement[8]} \n")
            text.insert(tk.END, f"  - Date de fin : {traitement[10]} \n")
        text.configure(state="disabled")
        ## Past ##
        # Title #
        label = tk.Label(self.traitementWindow, text="Anciens traitements :")
        label.pack(pady=10)
        # Info #
        text = tk.Text(self.traitementWindow, height=10, width=55)
        text.pack(pady=10)
        for traitement in PastTreatements:
            text.insert(tk.END, f"{traitement[7]}, {traitement[5]} : \n")
            text.insert(tk.END, f"  - Medicament DCI : {traitement[6]} \n")
            text.insert(tk.END, f"  - Medecin : {traitement[1]} \n")
            text.insert(tk.END, f"  - Pharmacien : {traitement[3]} \n")
            text.insert(tk.END, f"  - Durée : {traitement[9]} \n")
            text.insert(tk.END, f"  - Date de vente : {traitement[8]} \n")
            text.insert(tk.END, f"  - Date de fin : {traitement[10]} \n")
        text.configure(state="disabled")
        ## Return button ##
        buttonReturn = tk.Button(self.traitementWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.traitementWindow,self.clientWindow))
        buttonReturn.pack(pady=10)
        ## Conflicting ##
        if (len(ConflictingTreatements) > 0):
            messagebox.showwarning("Attention", "Le client t prend plusieurs médicaments du même type simultanément.\n Voici les médicaments concernés : " + str(ConflictingTreatements))
        else :
            messagebox.showinfo("Information", "Le client ne prend pas de médicaments du même type.")


    def consulterDiagnostic(self) :
        """Opens a window to consult the diagnostics of the client"""
        ### Get the info of the client ###
        self.cursor.execute(f"""SELECT dateDiagnostic, pathologieNom, specialite
                                FROM Diagnostic
                                WHERE NISS = {self.NISS}
                                ORDER BY pathologieNom DESC"""
                            )
        infoDiagnostic = self.cursor.fetchall()
        ### Create the new window ###
        self.clientWindow.withdraw()
        self.diagnosticWindow = tk.Toplevel(self.clientWindow)
        self.diagnosticWindow.title("Diagnostics")
        self.diagnosticWindow.geometry("500x500")
        self.diagnosticWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        ### Create the widgets ###
        ## texts ##
        # Title #
        label = tk.Label(self.diagnosticWindow, text="Diagnostics :")
        label.pack(pady=10)
        # Info #
        text = tk.Text(self.diagnosticWindow, height=20, width=55)
        text.pack(pady=10)
        for diagnostic in infoDiagnostic:
            text.insert(tk.END, f"{diagnostic[1]} : \n")
            text.insert(tk.END, f"  - Date : {diagnostic[0]} \n")
            text.insert(tk.END, f"  - Specialite : {diagnostic[2]} \n")
        text.configure(state="disabled")
        ## Return button ##
        buttonReturn = tk.Button(self.diagnosticWindow, text="Retour", width=20, command = lambda: self.returnToParentWindow(self.diagnosticWindow,self.clientWindow))
        buttonReturn.pack(pady=10)
        

    def returnToParentWindow(self,subwindow,root):
        """Returns to the parent window"""
        subwindow.destroy()
        root.deiconify()
    

    def isDateSqlFormat(self,date_string):
        """Checks if the date is in the correct format"""
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
        

    def isGSMFormat(self,GSM):
        """Checks if the GSM is in the correct format"""
        if GSM[0:2] == "04" :
            if len(GSM) != 10 :
                print("1")
                return False
        elif GSM[0:4] == "+324" :
            if len(GSM) != 12 :
                print("2")
                return False
        else :
            return False
        for i in range(2,10):
            if GSM[i] < '0' or GSM[i] > '9':
                return False
        return True
    

    def isEmailFormat(self,email):
        """Checks if the email is in the correct format"""
        if len(email) > 50 or len(email) < 5:
            print("1")
            return False
        elif email.find('@') == -1 or email.find('.') == -1:
            print("2")
            return False
        elif email.find('@') > email.rfind('.'):
            print("3")
            return False
        return True


if __name__ == '__main__':
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost',
        database='groupAX_DB'
    )
    cursor = cnx.cursor()
    myGUI = MyGUI(cursor, cnx)

