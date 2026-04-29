import customtkinter as ctk

class InterfaceMedecin(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#FAF9F6") # Fond crème officiel du logo

        # Titre de la section
        self.label = ctk.CTkLabel(self, text="📝 NOUVELLE PRESCRIPTION",
                                  font=("Arial", 22, "bold"), text_color="#284A48")
        self.label.pack(pady=20)

        # Formulaire structuré (Support à la décision clinique)
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40)

        # Liste des champs nécessaires pour une ordonnance propre
        champs = ["Nom du Médicament", "Dosage (ex: 500mg)", "Fréquence (ex: 2/jour)", "Durée"]
        for texte in champs:
            lbl = ctk.CTkLabel(self.form_frame, text=texte, font=("Arial", 12, "bold"), text_color="#284A48")
            lbl.pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.form_frame, placeholder_text=f"Saisir {texte.lower()}...",
                                 fg_color="#A3C4BC", border_color="#284A48", text_color="#284A48")
            entry.pack(fill="x", pady=5)

        # Bouton d'analyse des interactions avant signature
        self.btn_analyse = ctk.CTkButton(self, text="VÉRIFIER LES RISQUES ⚠️",
                                         fg_color="#2C8D65", hover_color="#1E5631", font=("Arial", 14, "bold"))
        self.btn_analyse.pack(pady=30, ipady=10)