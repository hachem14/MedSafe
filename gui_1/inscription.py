import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


# CTkToplevel = Fenêtre secondaire qui s'ouvre par dessus
class ApplicationInscription(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.BLEU_FONCE = "#0C3C4F"
        self.VERT_BOUCLIER = "#1A936F"
        self.FOND_CREME = "#F8F7F2"

        self.configure(fg_color=self.FOND_CREME)
        self.title("MedSafe - Inscription")
        self.geometry("450x700")

        self.attributes('-topmost', True)  # Reste au premier plan

        self.creer_interface()

    def creer_interface(self):
        try:
            image_logo = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), size=(220, 220))
            self.label_logo = ctk.CTkLabel(self, image=image_logo, text="")
            self.label_logo.pack(pady=(20, 10))
        except:
            self.label_logo = ctk.CTkLabel(self, text="Logo introuvable")
            self.label_logo.pack(pady=(30, 10))

        self.titre = ctk.CTkLabel(self, text="Créer un compte", font=("Arial", 26, "bold"), text_color=self.BLEU_FONCE)
        self.titre.pack(pady=10)

        self.champ_nom = ctk.CTkEntry(self, placeholder_text="Nom complet", font=("Arial", 14), width=300, height=45)
        self.champ_nom = ctk.CTkEntry(self, placeholder_text="Nom complet", font=("Arial", 14), width=300, height=45)
        self.champ_nom.pack(pady=10)

        self.champ_cni = ctk.CTkEntry(self, placeholder_text="N° de Carte Nationale (CNI)", font=("Arial", 14),
                                      width=300, height=45)
        self.champ_cni.pack(pady=10)

        self.champ_email = ctk.CTkEntry(self, placeholder_text="Email", font=("Arial", 14), width=300, height=45)
        self.champ_email.pack(pady=10)

        self.champ_mdp = ctk.CTkEntry(self, placeholder_text="Mot de passe", font=("Arial", 14), width=300, height=45,
                                      show="*")
        self.champ_mdp.pack(pady=10)

        self.bouton_inscrire = ctk.CTkButton(self, text="S'inscrire", font=("Arial", 16, "bold"), width=300, height=50,
                                             fg_color=self.VERT_BOUCLIER, command=self.valider_inscription)
        self.bouton_inscrire.pack(pady=20)

    def valider_inscription(self):
        nom = self.champ_nom.get()
        cni = self.champ_cni.get()

        if nom != "" and cni != "":
            messagebox.showinfo("Succès", f"Félicitations {nom} !\nVotre compte MedSafe est créé avec succès.")
            self.destroy()  # On ferme juste cette fenêtre, l'accueil est toujours là derrière !
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir au moins votre nom et votre n° de carte.")