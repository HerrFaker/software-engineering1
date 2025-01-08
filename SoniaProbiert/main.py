import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import simpledialog
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from planner.core import StudyMasterPlaner

class StudyMasterPlanerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Master Planer")
        self.planner = StudyMasterPlaner()

        # Standardkategorien definieren
        self.categories = ["Kurs", "Persönliche Aufgaben"]

        self.create_menu()
        self.create_task_input_section()
        self.create_task_view()

        # Zeige gespeicherte Aufgaben an
        self.refresh_task_view()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Datei-Menü
        #file_menu = tk.Menu(menu, tearoff=0)
        #menu.add_cascade(label="Datei", menu=file_menu)
        #file_menu.add_command(label="Beenden", command=self.root.quit)

        # Ansicht-Menü
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ansicht", menu=view_menu)
        view_menu.add_command(label="Kalenderansicht", command=self.show_calendar_view)
        view_menu.add_command(label="Listenansicht", command=self.show_list_view)

    def create_task_input_section(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=10, fill="x")  # Mehr Abstand um den gesamten Bereich

        # Eingabefelder für neue Aufgaben
        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.deadline_entry = tk.Entry(frame)
        self.deadline_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Priorität:").grid(row=2, column=0, padx=5, pady=5)
        self.priority_entry = tk.Entry(frame)
        self.priority_entry.grid(row=2, column=1, padx=5, pady=5)

        # Dropdown-Menü für Kategorien
        tk.Label(frame, text="Kategorie:").grid(row=3, column=0, padx=5, pady=5)
        self.selected_category = tk.StringVar()
        self.selected_category.set(self.categories[0])  # Standardkategorie
        self.category_menu = tk.OptionMenu(frame, self.selected_category, *self.categories)
        self.category_menu.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(frame)  # Extra Frame für die Buttons
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Button zum Hinzufügen von Aufgaben
        add_button = tk.Button(button_frame, text="Aufgabe hinzufügen", command=self.add_task, width=18, height=1)
        add_button.pack(side=tk.LEFT, padx=10)

        # Button zum Speichern der Änderungen
        save_button = tk.Button(button_frame, text="Änderungen speichern", command=self.update_task, width=18, height=1)
        save_button.pack(side=tk.LEFT, padx=10)

        # Button zum Löschen der ausgewählten Aufgabe
        delete_button = tk.Button(button_frame, text="Aufgabe löschen", command=self.delete_task, width=18, height=1)
        delete_button.pack(side=tk.LEFT, padx=10)

        # Button zum Hinzufügen neuer Kategorien
        add_category_button = tk.Button(button_frame, text="Kategorie hinzufügen", command=self.add_category, width=18, height=1)
        add_category_button.pack(side=tk.LEFT, padx=10)


    def create_task_view(self):
        """Erstellt die Treeview zur Anzeige der Aufgaben."""
        # Treeview konfigurieren
        self.tree = Treeview(self.root, columns=("Name", "Deadline", "Priorität", "category"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priorität", text="Priorität")
        self.tree.heading("category", text="category")

        # Spaltenbreite anpassen (optional)
        self.tree.column("Name", width=200)
        self.tree.column("Deadline", width=100)
        self.tree.column("Priorität", width=80)
        self.tree.column("category", width=100)

        # Treeview packen
        self.tree.pack(pady=10, fill="both", expand=True)
        
        # Bind Treeview-Auswahl an Methode
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def refresh_task_view(self):
        """Aktualisiert die Treeview mit den aktuellen Aufgaben."""
        tasks = self.planner.load_entries()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in tasks:
            self.tree.insert(
                "", "end",
                values=(task.name, task.deadline.strftime("%Y-%m-%d"), task.priority, task.category)
            )

    def on_treeview_select(self, event):
        """Lädt die ausgewählten Aufgaben-Daten in die Eingabefelder."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Hole die Werte aus der Treeview
        item = self.tree.item(selected_item[0], "values")
        name, deadline, priority, category = item

        # Werte in die Eingabefelder einfügen
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, deadline)

        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, priority)

        self.selected_category.set(category)



    def show_calendar_view(self):
        # Dummy-Methode für Kalenderansicht (kann angepasst werden)
        messagebox.showinfo("Kalenderansicht", "Kalenderansicht wird hier angezeigt!")

    def show_list_view(self):
        # Dummy-Methode für Listenansicht (aktuell aktualisiert sie nur die Ansicht)
        self.refresh_task_view()
        
    def add_category(self):
        """Fügt eine neue Kategorie hinzu."""
        new_category = tk.simpledialog.askstring("Neue Kategorie", "Gib den Namen der neuen Kategorie ein:")
        if new_category:
            if new_category not in self.categories:
                self.categories.append(new_category)
                self.category_menu['menu'].add_command(label=new_category, command=tk._setit(self.selected_category, new_category))
                messagebox.showinfo("Erfolg", f"Die Kategorie '{new_category}' wurde hinzugefügt!")
            else:
                messagebox.showerror("Fehler", f"Die Kategorie '{new_category}' existiert bereits.")


    def add_task(self):
        """Fügt eine neue Aufgabe hinzu und aktualisiert die Anzeige."""
        try:
            # Eingaben aus den Feldern lesen
            name = self.name_entry.get()
            deadline = datetime.strptime(self.deadline_entry.get(), "%Y-%m-%d")
            priority = int(self.priority_entry.get())
            category = self.selected_category.get()

            # Aufgabe erstellen
            self.planner.create_entry(name, deadline, priority, category)

            # Aktualisiere die Treeview
            self.refresh_task_view()

            # Eingabefelder leeren
            self.name_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich hinzugefügt!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            
    def update_task(self):
        """Speichert die geänderten Daten der ausgewählten Aufgabe."""
        try:
            # Hole den ausgewählten Aufgaben-Namen
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
                return

            old_name = self.tree.item(selected_item[0], "values")[0]  # Name der Aufgabe vor Änderung

            # Werte aus den Eingabefeldern lesen
            new_name = self.name_entry.get()
            new_deadline = datetime.strptime(self.deadline_entry.get(), "%Y-%m-%d")
            new_priority = int(self.priority_entry.get())
            new_category = self.selected_category.get()


            # Bearbeitung der Aufgabe
            if old_name == new_name:
                # Wenn der Name nicht geändert wurde, nur die Felder aktualisieren
                self.planner.edit_entry(new_name, "deadline", new_deadline)
                self.planner.edit_entry(new_name, "priority", new_priority)
                self.planner.edit_entry(new_name, "category", new_category)
            else:
                # Wenn der Name geändert wurde, alte Aufgabe löschen und neue erstellen
                self.planner.delete_entry(old_name)
                self.planner.create_entry(new_name, new_deadline, new_priority, new_category)

            # Treeview aktualisieren
            self.refresh_task_view()
            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich aktualisiert!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            
    def delete_task(self):
        """Löscht die ausgewählte Aufgabe."""
        try:
            # Hole die ausgewählte Zeile in der Treeview
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
                return

            # Hole den Namen der Aufgabe aus der Treeview
            task_name = self.tree.item(selected_item[0], "values")[0]

            # Aufgabe aus dem Planer und der Datenbank löschen
            self.planner.delete_entry(task_name)

            # Aktualisiere die Treeview
            self.refresh_task_view()

            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", f"Die Aufgabe '{task_name}' wurde gelöscht!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))


# Hauptprogramm starten
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyMasterPlanerUI(root)
    root.mainloop()
