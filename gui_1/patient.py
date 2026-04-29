import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class InterfacePatient(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.BLEU_FONCE = "#0C3C4F"
        self.VERT_BOUCLIER = "#1A936F"
        self.FOND_CREME = "#F8F7F2"

        self.configure(fg_color=self.FOND_CREME)
        self.title("MedSafe - Dossier Patient")
        # J'ai agrandi la hauteur à 800 pour laisser de la place à la grande case
        self.geometry("500x800")

        self.attributes('-topmost', True)

        self.creer_interface()

    def creer_interface(self):
        try:
            image_logo = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), size=(160, 160))
            self.label_logo = ctk.CTkLabel(self, image=image_logo, text="")
            self.label_logo.pack(pady=(20, 10))
        except:
            self.label_logo = ctk.CTkLabel(self, text="Logo introuvable")
            self.label_logo.pack(pady=(20, 10))

        self.titre = ctk.CTkLabel(self, text="Nouveau Dossier Patient", font=("Arial", 24, "bold"),
                                  text_color=self.BLEU_FONCE)
        self.titre.pack(pady=10)

        self.champ_nom = ctk.CTkEntry(self, placeholder_text="Nom et Prénom du patient", font=("Arial", 14), width=350,
                                      height=45)
        self.champ_nom.pack(pady=10)

        self.champ_age = ctk.CTkEntry(self, placeholder_text="Âge", font=("Arial", 14), width=350, height=45)
        self.champ_age.pack(pady=10)

        self.champ_poids = ctk.CTkEntry(self, placeholder_text="Poids (en kg)", font=("Arial", 14), width=350,
                                        height=45)
        self.champ_poids.pack(pady=10)

        self.champ_maladies = ctk.CTkEntry(self, placeholder_text="Maladies chroniques", font=("Arial", 14), width=350,
                                           height=45)
        self.champ_maladies.pack(pady=10)

        # --- NOUVELLE CASE : DESCRIPTION ÉLARGIE ---
        # 1. On met un petit titre pour expliquer à l'utilisateur
        self.label_desc = ctk.CTkLabel(self, text="Description (Notes, allergies, symptômes...) :",
                                       font=("Arial", 14, "bold"), text_color=self.BLEU_FONCE)
        self.label_desc.pack(pady=(10, 0))

        # 2. On utilise CTkTextbox pour avoir une case bien large et haute (height=120)
        self.champ_description = ctk.CTkTextbox(self, font=("Arial", 14), width=350, height=120, border_width=2,
                                                border_color=self.VERT_BOUCLIER)
        self.champ_description.pack(pady=(5, 10))

        self.bouton_enregistrer = ctk.CTkButton(self, text="Enregistrer le patient", font=("Arial", 16, "bold"),
                                                width=350, height=50, fg_color=self.VERT_BOUCLIER,
                                                command=self.valider_patient)
        self.bouton_enregistrer.pack(pady=20)

    def valider_patient(self):
        nom = self.champ_nom.get()

        if nom != "":
            messagebox.showinfo("Succès", f"Le dossier médical de {nom} a été créé avec succès !")
            self.destroy()  # Ferme uniquement la fenêtre patient et redonne la main à l'accueil
        else:
            messagebox.showwarning("Erreur", "Veuillez au moins renseigner le nom du patient.")
            messagebox.showwarning("Erreur", "Veuillez au moins renseigner le nom du patient.")