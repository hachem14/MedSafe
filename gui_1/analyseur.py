import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import json
import os


class AnalyseurRisques(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, fg_color="transparent", *args, **kwargs)

        # Couleurs officielles MedSafe extraites du logo
        self.BLEU_FONCE = "#0A3D4D"
        self.VERT_BOUCLIER = "#2D8B6F"
        self.INPUT_BG = "#E8EFED"

        self.liste_A = []
        self.liste_B = []

        # 1. Charger les données du fichier JSON
        self.medicaments_data = self.charger_base_json()
        self.noms_medics = [m["nom"] for m in self.medicaments_data]

        self.creer_interface()

    def charger_base_json(self):
        """Charge la base de données locale des médicaments[cite: 1197, 1221]."""
        # Note : Vérifiez bien que le nom correspond à votre fichier .json
        nom_fichier = "bas_med.json"
        if os.path.exists(nom_fichier):
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def creer_interface(self):
        self.titre = ctk.CTkLabel(self, text="Vérificateur d'Interactions", font=("Arial", 28, "bold"),
                                  text_color=self.BLEU_FONCE)
        self.titre.pack(pady=(20, 10))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=10)

        # --- PANEL A ---
        self.frame_A = ctk.CTkFrame(container, fg_color=self.INPUT_BG, corner_radius=15)
        self.frame_A.grid(row=0, column=0, padx=15, pady=10)
        ctk.CTkLabel(self.frame_A, text="Médicaments Actuels", font=("Arial", 14, "bold")).pack(pady=5)

        self.entry_A = ctk.CTkEntry(self.frame_A, placeholder_text="Chercher...", width=200)
        self.entry_A.pack(pady=5, padx=10)
        self.entry_A.bind("<KeyRelease>", lambda e: self.update_autocomplete(e, "A"))

        ctk.CTkButton(self.frame_A, text="+ Ajouter", fg_color=self.BLEU_FONCE, command=self.ajouter_A).pack(pady=5)
        self.box_A = ctk.CTkTextbox(self.frame_A, width=200, height=100)
        self.box_A.pack(pady=10, padx=10)

        # --- PANEL B ---
        self.frame_B = ctk.CTkFrame(container, fg_color=self.INPUT_BG, corner_radius=15)
        self.frame_B.grid(row=0, column=1, padx=15, pady=10)
        ctk.CTkLabel(self.frame_B, text="Nouveaux Médicaments", font=("Arial", 14, "bold")).pack(pady=5)

        self.entry_B = ctk.CTkEntry(self.frame_B, placeholder_text="Chercher...", width=200)
        self.entry_B.pack(pady=5, padx=10)
        self.entry_B.bind("<KeyRelease>", lambda e: self.update_autocomplete(e, "B"))

        ctk.CTkButton(self.frame_B, text="+ Ajouter", fg_color=self.BLEU_FONCE, command=self.ajouter_B).pack(pady=5)
        self.box_B = ctk.CTkTextbox(self.frame_B, width=200, height=100)
        self.box_B.pack(pady=10, padx=10)

        # --- LISTBOX D'AUTOCOMPLÉTION (Flottante) ---
        self.listbox = tk.Listbox(self, font=("Arial", 11), height=5, relief="flat", bg="white")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.btn_analyse = ctk.CTkButton(self, text="🚨 Lancer l'Analyse", width=400, height=45,
                                         fg_color=self.VERT_BOUCLIER, command=self.lancer_analyse)
        self.btn_analyse.pack(pady=10)

        self.boite_resultat = ctk.CTkTextbox(self, width=580, height=150, border_width=2,
                                             border_color=self.VERT_BOUCLIER)
        self.boite_resultat.pack(pady=10)

    # --- LOGIQUE D'AUTOCOMPLÉTION [cite: 1205, 1208] ---
    def update_autocomplete(self, event, liste_type):
        self.active_list = liste_type
        entry = self.entry_A if liste_type == "A" else self.entry_B
        typed = entry.get().upper()

        if typed == '':
            self.listbox.place_forget()
        else:
            matches = [m for m in self.noms_medics if typed in m.upper()]
            if matches:
                self.listbox.delete(0, "end")
                for m in matches:
                    self.listbox.insert("end", m)

                # Positionnement dynamique sous l'Entry active
                x_pos = entry.winfo_x() + (entry.master.winfo_x())
                self.listbox.place(x=x_pos + 15, y=160, width=200)
            else:
                self.listbox.place_forget()

    def on_select(self, event):
        if self.listbox.curselection():
            selection = self.listbox.get(self.listbox.curselection())
            if self.active_list == "A":
                self.entry_A.delete(0, "end")
                self.entry_A.insert(0, selection)
            else:
                self.entry_B.delete(0, "end")
                self.entry_B.insert(0, selection)
            self.listbox.place_forget()

    def ajouter_A(self):
        med = self.entry_A.get().upper().strip()
        if med in self.noms_medics:
            if med not in self.liste_A:
                self.liste_A.append(med)
                self.box_A.insert("end", f"• {med}\n")
            self.entry_A.delete(0, "end")
        else:
            messagebox.showwarning("Inconnu", "Veuillez sélectionner un médicament de la liste.")

    def ajouter_B(self):
        med = self.entry_B.get().upper().strip()
        if med in self.noms_medics:
            if med not in self.liste_B:
                self.liste_B.append(med)
                self.box_B.insert("end", f"• {med}\n")
            self.entry_B.delete(0, "end")
        else:
            messagebox.showwarning("Inconnu", "Veuillez sélectionner un médicament de la liste.")

    def lancer_analyse(self):
        """Compare les substances pour détecter les risques[cite: 1200, 1202]."""
        self.boite_resultat.delete("1.0", "end")
        if not self.liste_A or not self.liste_B:
            self.boite_resultat.insert("end", "⚠️ Veuillez remplir les deux listes.")
            return

        conflit = False
        for m_a in self.liste_A:
            data_a = next(x for x in self.medicaments_data if x["nom"] == m_a)
            for m_b in self.liste_B:
                data_b = next(x for x in self.medicaments_data if x["nom"] == m_b)

                # Détection par substance active (ex: Doliprane + Dafalgan = Surdosage Paracétamol)
                if data_a["substance"] == data_b["substance"]:
                    conflit = True
                    self.boite_resultat.insert("end", f"🚨 ALERTE SURDOSAGE : {m_a} + {m_b}\n")
                    self.boite_resultat.insert("end", f"Substance commune : {data_a['substance']}\n")
                    self.boite_resultat.insert("end", f"Note : {data_a['limitation']}\n")
                    self.boite_resultat.insert("end", f"Dose Max : {data_a['dose_maximale']}\n\n")

        if not conflit:
            self.boite_resultat.insert("end",
                                       "✅ Aucune interaction par substance trouvée.\nLes médicaments semblent compatibles.")