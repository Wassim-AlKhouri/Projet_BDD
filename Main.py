import tkinter as tk
from tkinter import messagebox
import mysql.connector

class MyGUI():
    def __init__(self,cursor):
        self.cursor = cursor
        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.title("Groupe AX")
        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.filemenu = tk.Menu(self.root, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)

        self.queriesmenu = tk.Menu(self.root, tearoff=0)
        #for i in range(1,11):
        #    self.queriesmenu.add_command(label=f"Query {i}", command=lambda: self.launch_query(i))
        self.queriesmenu.add_command(label=f"Query 1", command=lambda: self.launch_query(1))
        self.queriesmenu.add_command(label=f"Query 2", command=lambda: self.launch_query(2))
        self.queriesmenu.add_command(label=f"Query 3", command=lambda: self.launch_query(3))
        self.queriesmenu.add_command(label=f"Query 4", command=lambda: self.launch_query(4))
        self.queriesmenu.add_command(label=f"Query 5", command=lambda: self.launch_query(5))
        self.queriesmenu.add_command(label=f"Query 6", command=lambda: self.launch_query(6))
        self.queriesmenu.add_command(label=f"Query 7", command=lambda: self.launch_query(7))
        self.queriesmenu.add_command(label=f"Query 8", command=lambda: self.launch_query(8))
        self.queriesmenu.add_command(label=f"Query 9", command=lambda: self.launch_query(9))
        self.queriesmenu.add_command(label=f"Query 10", command=lambda: self.launch_query(10))
    
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Queries", menu=self.queriesmenu)
        self.root.config(menu=self.menubar)

        self.text = tk.Label(self.root, text="Connection", font=("Helvetica", 16), pady=20)
        self.text.pack()

        self.entryUser = tk.Entry(self.root, width=30, justify="center")
        self.entryUser.insert(0, "Username")
        self.entryUser.bind("<FocusIn>", lambda event, arg="Username": self.clear_default_entry(event, arg))
        self.entryUser.pack(pady=10)

        self.entryPassword = tk.Entry(self.root, width=30, justify="center")
        self.entryPassword.insert(0, "Password")
        self.entryPassword.bind("<FocusIn>", lambda event, arg="Password": self.clear_default_entry(event, arg))
        self.entryPassword.pack(pady=10)

        self.button = tk.Button(self.root, text="Connect", width=20, command=self.connect)
        self.button.pack(pady=10)

        self.root.mainloop()

    def launch_query(self,number):
        """Launches the query"""
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Query {number}")
        new_window.geometry("600x600")
        entry1 = tk.Entry(new_window, width=30, justify="center")
        entry2 = tk.Entry(new_window, width=30, justify="center")
        entriesToShow = []
        match number:
            case 1:
                description = "La liste des noms commerciaux de médicaments correspondant à un nom en DCI, classés par ordre alphabétique et taille de conditionnement."
                
                entry1.insert(0, "DCI")
                entry1.bind("<FocusIn>", lambda event, arg="DCI": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)
            case 2:
                description = "La liste des pathologies qui peuvent être prise en charge par un seul type de spécialistes"
                
                entry1.insert(0, "specialite")
                entry1.bind("<FocusIn>", lambda event, arg="specialite": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)
            case 3:
                description = "La spécialité de médecins pour laquelle les médecins prescrivent le plus de médicaments"
            case 4:
                description = "Tous les utilisateurs ayant consommé un médicament spécifique (sous son nom commercial) après une date donnée, par exemple en cas de rappel de produit pour lot contaminé"
                
                entry1.insert(0, "NomCommercial")
                entry1.bind("<FocusIn>", lambda event, arg="NomCommercial": self.clear_default_entry(event, arg))
                entry2.insert(0, "Date De Prescription (YYYY-MM-DD)")
                entry2.bind("<FocusIn>", lambda event, arg="Date De Prescription (YYYY-MM-DD)": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)
                entriesToShow.append(entry2)
            case 5:
                description = "Tous les  patients ayant été traités par un médicament (sous sa DCI) à une date antérieure mais qui ne le sont plus,pour vérifier qu’un patient suive bien un traitement chronique"
                
                entry1.insert(0, "DCI")
                entry1.bind("<FocusIn>", lambda event, arg="DCI": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)
            case 6:
                description = "La liste des médecins ayant prescrit des médicaments ne relevant pas de leur spécialité"
            case 7:
                description = "Pour chaque décennie entre 1950 et 2020,(1950−59,1960−69,...),le médicament le plus consommé par des patients nés durant cette décennie"
            case 8:
                description = "Quelle est la pathologie la plus diagnostiquée"
            case 9:
                description = "Pour chaque patient,le nombre de médecin lui ayant prescrit un médicament "

                entry1.insert(0, "NISS")
                entry1.bind("<FocusIn>", lambda event, arg="NISS": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)
            case 10:
                description = "La liste de médicament n’étant plus prescrit depuis une date spécifique"

                entry1.insert(0, "Date de prescription (YYYY-MM-DD)")
                entry1.bind("<FocusIn>", lambda event, arg="Date de prescription (YYYY-MM-DD)": self.clear_default_entry(event, arg))
                entriesToShow.append(entry1)

        text = tk.Text(new_window, height=5, width=50,wrap="word")
        text.insert(tk.END,description)
        text.configure(state="disabled")
        text.pack()
        
        for entry in entriesToShow:
            entry.pack(pady=10)

        button = tk.Button(new_window, text="Launch", width=20, command=lambda: self.launch_quary(number,self.cursor,[entry.get() for entry in entriesToShow]))
        button.pack(pady=10)
        

    def connect(self):
        """Connects to the database"""
        pass

    def clear_default_entry(self, event, arg):
        """Clears the default text in the entry widget when clicked on"""
        if event.widget.get() == arg:
            event.widget.delete(0, tk.END)

    def on_closing(self):
        """Asks the user if he wants to quit the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

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


if __name__ == '__main__':
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost',
        database='groupAX_DB'
    )
    cursor = cnx.cursor()
    myGUI = MyGUI(cursor)

