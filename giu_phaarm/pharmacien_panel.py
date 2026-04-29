import customtkinter as ctk


class InterfacePharmacien(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#FAF9F6")

        # Titre Dashboard
        self.label = ctk.CTkLabel(self, text="💊 DASHBOARD PHARMACIEN",
                                  font=("Arial", 22, "bold"), text_color="#284A48")
        self.label.pack(pady=20)

        # Barre de recherche rapide de patient (via CNI ou Nom)
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=40)

        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher Patient (CNI / Nom)...",
                                         fg_color="#FFFFFF", border_color="#2C8D65", width=400)
        self.entry_search.pack(side="left", padx=(0, 10))

        self.btn_search = ctk.CTkButton(self.search_frame, text="RECHERCHER", fg_color="#284A48", width=100)
        self.btn_search.pack(side="left")

        # Zone d'affichage des alertes cliniques (Analyse DDInter)
        self.alert_box = ctk.CTkTextbox(self, height=250, fg_color="#FFFFFF", border_color="#2C8D65", border_width=2)
        self.alert_box.pack(fill="both", padx=40, pady=20)
        self.alert_box.insert("0.0", "--- PRÊT POUR ANALYSE DE DÉLIVRANCE ---\nEn attente de sélection de patient...")

        # Bouton d'exportation pour archive (Phase 2 du projet)
        self.btn_export = ctk.CTkButton(self, text="GÉNÉRER RAPPORT PDF 📄", fg_color="#2C8D65")
        self.btn_export.pack(pady=10)