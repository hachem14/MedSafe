from gui_1.inscription import ApplicationInscription
from gui_1.patient import InterfacePatient


class MedSafeController:
    def __init__(self):
        # On commence par lancer l'écran d'inscription [cite: 348]
        self.lancer_inscription()

    def lancer_inscription(self):
        self.ecran_inscription = ApplicationInscription()

        # On intercepte le clic sur le bouton pour changer de page
        # au lieu de juste afficher un message [cite: 365, 367]
        self.ecran_inscription.bouton_inscrire.configure(command=self.vers_patient)
        self.ecran_inscription.mainloop()

    def vers_patient(self):
        # 1. On valide d'abord les données de l'inscription [cite: 24]
        self.ecran_inscription.valider_inscription()

        # 2. On ferme la fenêtre d'inscription
        self.ecran_inscription.destroy()

        # 3. On ouvre la fenêtre du dossier patient [cite: 362]
        self.ecran_patient = InterfacePatient()
        self.ecran_patient.mainloop()


if __name__ == "__main__":
    # C'est ici que l'aventure MedSafe commence ! [cite: 105]
    app = MedSafeController()