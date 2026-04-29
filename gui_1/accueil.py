import customtkinter as ctk
from PIL import Image
import os

class MedSafeHome(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MedSafe - Tableau de Bord Principal")

        # Dimensions de la fenêtre
        # Dimensions de la fenêtre
        width = self.winfo_screenwidth() * 0.8
        height = self.winfo_screenheight() * 0.8
        self.geometry(f"{int(width)}x{int(height)}")

        # Palette de couleurs MedSafe
        self.bg_color = "#F7F3E9"
        self.primary_green = "#2D8B6F"
        self.dark_teal = "#0A3D4D"
        self.configure(fg_color=self.bg_color)

        # Configuration de la grille : 2 colonnes (Menu à gauche, Contenu à droite)
        self.grid_columnconfigure(1, weight=1) # La colonne 1 (droite) prend tout l'espace restant
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # 1. LE MENU LATÉRAL (SIDEBAR) À GAUCHE
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.dark_teal)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Pousse les éléments vers le haut

        # Logo dans le menu
        if os.path.exists("mokkt.jpg"):
            self.logo_image = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), size=(120, 120))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
            self.logo_label.grid(row=0, column=0, pady=(30, 10))

        self.titre_menu = ctk.CTkLabel(self.sidebar_frame, text="MEDSAFE", font=("Arial", 22, "bold"), text_color="white")
        self.titre_menu.grid(row=1, column=0, pady=(0, 30))

        # Les 4 Boutons de Fonctionnalités
        self.btn_accueil = ctk.CTkButton(self.sidebar_frame, text="1. Accueil", fg_color="transparent",
                                         hover_color=self.primary_green, font=("Arial", 16, "bold"), anchor="w",
                                         command=self.afficher_accueil)
        self.btn_accueil.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        self.btn_inscription = ctk.CTkButton(self.sidebar_frame, text="2. Inscription", fg_color="transparent",
                                             hover_color=self.primary_green, font=("Arial", 16, "bold"), anchor="w",
                                             command=self.afficher_inscription)
        self.btn_inscription.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

        self.btn_patient = ctk.CTkButton(self.sidebar_frame, text="3. Dossier Patient", fg_color="transparent",
                                         hover_color=self.primary_green, font=("Arial", 16, "bold"), anchor="w",
                                         command=self.afficher_patient)
        self.btn_patient.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

        self.btn_analyse = ctk.CTkButton(self.sidebar_frame, text="4. Analyseur Risques", fg_color="transparent",
                                         hover_color=self.primary_green, font=("Arial", 16, "bold"), anchor="w",
                                         command=self.afficher_analyse)
        self.btn_analyse.grid(row=5, column=0, pady=10, padx=20, sticky="ew")

        # ==========================================
        # 2. LA ZONE DE CONTENU PRINCIPAL À DROITE
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_color)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # On affiche la page d'accueil par défaut au lancement
        self.afficher_accueil()

    # --- MÉTHODES DE NAVIGATION (TRANSLATION) ---

    def nettoyer_ecran(self):
        """Supprime tout le contenu actuel de la zone de droite avant d'afficher le nouveau."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def afficher_accueil(self):
        self.nettoyer_ecran()
        titre = ctk.CTkLabel(self.main_frame, text="Plateforme de Gestion Pharmaceutique", font=("Helvetica", 35, "bold"), text_color=self.dark_teal)
        titre.pack(pady=(100, 20))
        desc = ctk.CTkLabel(self.main_frame, text="Sélectionnez une fonctionnalité dans le menu de gauche pour commencer.", font=("Helvetica", 18), text_color="gray")
        desc.pack()

    def afficher_inscription(self):
        self.nettoyer_ecran()
        titre = ctk.CTkLabel(self.main_frame, text="Création de Compte", font=("Helvetica", 35, "bold"), text_color=self.dark_teal)
        titre.pack(pady=(100, 20))
        info = ctk.CTkLabel(self.main_frame, text="(L'interface d'inscription s'affichera ici)", font=("Arial", 16))
        info.pack()

    def afficher_patient(self):
        self.nettoyer_ecran()
        titre = ctk.CTkLabel(self.main_frame, text="Nouveau Dossier Patient", font=("Helvetica", 35, "bold"), text_color=self.dark_teal)
        titre.pack(pady=(100, 20))
        info = ctk.CTkLabel(self.main_frame, text="(Le formulaire patient s'affichera ici)", font=("Arial", 16))
        info.pack()

    def afficher_analyse(self):
        self.nettoyer_ecran()
        titre = ctk.CTkLabel(self.main_frame, text="Analyse des Interactions (DDInter)", font=("Helvetica", 35, "bold"), text_color=self.dark_teal)
        titre.pack(pady=(100, 20))
        info = ctk.CTkLabel(self.main_frame, text="(Le moteur de recherche des médicaments s'affichera ici)", font=("Arial", 16))
        info.pack()

if __name__ == "__main__":
    app = MedSafeHome()
    app.mainloop()