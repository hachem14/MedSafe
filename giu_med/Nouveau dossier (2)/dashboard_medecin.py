import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import messagebox, filedialog


# =========================================================
# 1. FENÊTRE DE CONNEXION ET INSCRIPTION
# =========================================================
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEDSAFE - Authentification")
        self.geometry("500x700")
        self.configure(fg_color="#FAF9F6")  # Fond crème

        self.connexion_reussie = False
        self.medecin_data = None

        self.afficher_login()

    def nettoyer(self):
        for widget in self.winfo_children():
            widget.destroy()

    def ajouter_logo(self):
        try:
            logo_image = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), dark_image=Image.open("mokkt.jpg"),
                                      size=(120, 120))
            ctk.CTkLabel(self, image=logo_image, text="").pack(pady=(40, 10))
        except Exception:
            ctk.CTkLabel(self, text="⚠️ MEDSAFE", font=("Arial", 30, "bold"), text_color="#284A48").pack(pady=(40, 10))

    def afficher_login(self):
        self.nettoyer()
        self.ajouter_logo()

        ctk.CTkLabel(self, text="CONNEXION", font=("Arial", 24, "bold"), text_color="#284A48").pack(pady=(10, 30))

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Adresse Email", width=300, fg_color="#FFFFFF",
                                        text_color="#284A48")
        self.entry_email.pack(pady=10)

        self.entry_mdp = ctk.CTkEntry(self, placeholder_text="Mot de passe", width=300, fg_color="#FFFFFF",
                                      text_color="#284A48", show="*")
        self.entry_mdp.pack(pady=10)

        ctk.CTkButton(self, text="SE CONNECTER", width=300, fg_color="#2C8D65", hover_color="#1E5631",
                      font=("Arial", 15, "bold"), command=self.verifier_login).pack(pady=20)

        ctk.CTkLabel(self, text="Vous n'avez pas de compte ?", text_color="gray").pack(pady=(20, 0))
        ctk.CTkButton(self, text="CRÉER UN COMPTE", width=300, fg_color="transparent", border_color="#284A48",
                      border_width=2, text_color="#284A48", command=self.afficher_inscription).pack(pady=10)

    def afficher_inscription(self):
        self.nettoyer()
        self.ajouter_logo()

        ctk.CTkLabel(self, text="CRÉER UN COMPTE MÉDECIN", font=("Arial", 20, "bold"), text_color="#284A48").pack(
            pady=(10, 20))

        self.reg_nom = ctk.CTkEntry(self, placeholder_text="Nom Complet (ex: Dr. Benali)", width=300,
                                    fg_color="#FFFFFF", text_color="#284A48")
        self.reg_nom.pack(pady=8)

        self.reg_spec = ctk.CTkEntry(self, placeholder_text="Spécialité (ex: Cardiologue)", width=300,
                                     fg_color="#FFFFFF", text_color="#284A48")
        self.reg_spec.pack(pady=8)

        self.reg_email = ctk.CTkEntry(self, placeholder_text="Adresse Email", width=300, fg_color="#FFFFFF",
                                      text_color="#284A48")
        self.reg_email.pack(pady=8)

        self.reg_mdp = ctk.CTkEntry(self, placeholder_text="Mot de passe", width=300, fg_color="#FFFFFF",
                                    text_color="#284A48", show="*")
        self.reg_mdp.pack(pady=8)

        ctk.CTkButton(self, text="S'INSCRIRE", width=300, fg_color="#2C8D65", hover_color="#1E5631",
                      font=("Arial", 15, "bold"), command=self.enregistrer_medecin).pack(pady=20)

        ctk.CTkButton(self, text="⬅️ Retour à la connexion", width=300, fg_color="transparent", text_color="#284A48",
                      command=self.afficher_login).pack(pady=10)

    def verifier_login(self):
        email = self.entry_email.get()
        mdp = self.entry_mdp.get()

        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medecins WHERE email = ? AND mot_de_passe = ?", (email, mdp))
            medecin = cursor.fetchone()
            conn.close()

            if medecin:
                self.medecin_data = medecin
                self.connexion_reussie = True
                self.destroy()
            else:
                messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        except Exception as e:
            messagebox.showerror("Erreur SQL", f"Problème de base de données : {e}")

    def enregistrer_medecin(self):
        nom = self.reg_nom.get()
        spec = self.reg_spec.get()
        email = self.reg_email.get()
        mdp = self.reg_mdp.get()

        if not nom or not email or not mdp:
            messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires.")
            return

        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS medecins (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, specialite TEXT, email TEXT UNIQUE, mot_de_passe TEXT)''')

            cursor.execute("INSERT INTO medecins (nom, specialite, email, mot_de_passe) VALUES (?, ?, ?, ?)",
                           (nom, spec, email, mdp))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès 🎉", "Compte créé avec succès ! Connectez-vous.")
            self.afficher_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Cet email est déjà utilisé !")
        except Exception as e:
            print(f"Erreur SQL : {e}")


# =========================================================
# 2. LE TABLEAU DE BORD PRINCIPAL
# =========================================================
class DashboardMedecin(ctk.CTk):
    def __init__(self, medecin_connecte):
        super().__init__()
        self.medecin_info = medecin_connecte

        self.title("MEDSAFE - Espace Médecin")
        self.geometry("1200x800")
        self.configure(fg_color="#FAF9F6")

        # --- MENU LATÉRAL (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#284A48")
        self.sidebar.pack(side="left", fill="y")

        try:
            logo_image = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), dark_image=Image.open("mokkt.jpg"),
                                      size=(150, 150))
            self.logo_label = ctk.CTkLabel(self.sidebar, image=logo_image, text="")
            self.logo_label.pack(pady=(30, 10))
        except Exception:
            self.logo_label = ctk.CTkLabel(self.sidebar, text="⚠️ Logo", text_color="red")
            self.logo_label.pack(pady=(30, 10))

        self.titre_label = ctk.CTkLabel(self.sidebar, text="👨‍⚕️ ESPACE MÉDECIN", font=("Arial", 18, "bold"),
                                        text_color="#FAF9F6")
        self.titre_label.pack(pady=(0, 20))

        self.creer_bouton_menu("👤 Mon Profil", self.afficher_profil)
        self.creer_bouton_menu("🗂️ Gestion Malades", self.afficher_malades)
        self.creer_bouton_menu("📓 Journal Médical", self.afficher_journal)
        self.creer_bouton_menu("📝 Ordonnance Libre", self.afficher_ordonnance)
        self.creer_bouton_menu("🩺 Gestion Équipements", self.afficher_equipement)

        # --- ZONE DE CONTENU PRINCIPALE ---
        self.zone_droite = ctk.CTkFrame(self, fg_color="transparent")
        self.zone_droite.pack(side="right", fill="both", expand=True)

        self.zone_contenu = ctk.CTkFrame(self.zone_droite, fg_color="#FAF9F6", corner_radius=0)
        self.zone_contenu.pack(side="top", fill="both", expand=True)

        # --- PANNEAU PUBLICITAIRE ---
        self.ad_frame = ctk.CTkFrame(self.zone_droite, height=120, fg_color="#E8F5E9", border_color="#2C8D65",
                                     border_width=2)
        self.ad_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        ctk.CTkLabel(self.ad_frame, text="🌟 ESPACE SPONSOR / PUBLICITÉ PHARMACEUTIQUE 🌟", font=("Arial", 16, "bold"),
                     text_color="#284A48").pack(pady=(20, 5))
        ctk.CTkLabel(self.ad_frame, text="Découvrez le nouveau stéthoscope connecté de notre partenaire...",
                     font=("Arial", 12), text_color="#555555").pack()

        self.afficher_profil()

    def creer_bouton_menu(self, texte, commande):
        bouton = ctk.CTkButton(self.sidebar, text=texte, command=commande, fg_color="transparent",
                               hover_color="#2C8D65", font=("Arial", 15, "bold"), anchor="w")
        bouton.pack(fill="x", padx=20, pady=10)
        return bouton

    def nettoyer_contenu(self):
        for widget in self.zone_contenu.winfo_children():
            widget.destroy()

    # --- 0. PROFIL CONNECTÉ ---
    def afficher_profil(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="👤 MON PROFIL PROFESSIONNEL", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 30))

        nom = self.medecin_info[1]
        specialite = self.medecin_info[2]
        email = self.medecin_info[3]

        carte_profil = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        carte_profil.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(carte_profil, text=f"🩺 {nom}", font=("Arial", 22, "bold"), text_color="#284A48").pack(
            pady=(20, 10), anchor="w", padx=30)
        ctk.CTkLabel(carte_profil, text=f"Spécialité : {specialite}", font=("Arial", 16), text_color="#284A48").pack(
            pady=5, anchor="w", padx=30)
        ctk.CTkLabel(carte_profil, text=f"Email : {email}", font=("Arial", 16), text_color="#284A48").pack(pady=(5, 20),
                                                                                                           anchor="w",
                                                                                                           padx=30)

        ctk.CTkButton(self.zone_contenu, text="🔴 SE DÉCONNECTER", fg_color="#D32F2F", hover_color="#B71C1C",
                      font=("Arial", 14, "bold"), command=self.deconnexion).pack(pady=40)

    def deconnexion(self):
        self.destroy()

    # --- 1. GESTION DES MALADES ---
    def afficher_malades(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="🗂️ GESTION DES MALADES", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 10))
        toolbar = ctk.CTkFrame(self.zone_contenu, fg_color="transparent")
        toolbar.pack(fill="x", padx=40, pady=10)
        self.entry_recherche = ctk.CTkEntry(toolbar, placeholder_text="Chercher par CNI ou Nom...", width=300,
                                            fg_color="#FFFFFF", text_color="#284A48")
        self.entry_recherche.pack(side="left", padx=(0, 10))
        ctk.CTkButton(toolbar, text="🔍 CHERCHER", fg_color="#284A48", command=self.rechercher_patients).pack(
            side="left")
        ctk.CTkButton(toolbar, text="➕ NOUVEAU PATIENT", fg_color="#2C8D65", hover_color="#1E5631",
                      command=self.afficher_formulaire_patient).pack(side="right")
        self.liste_patients_frame = ctk.CTkScrollableFrame(self.zone_contenu, fg_color="#E8F5E9",
                                                           border_color="#2C8D65", border_width=2)
        self.liste_patients_frame.pack(fill="both", expand=True, padx=40, pady=20)
        self.charger_patients()

    def rechercher_patients(self):
        self.charger_patients(self.entry_recherche.get())

    def charger_patients(self, recherche=""):
        for widget in self.liste_patients_frame.winfo_children():
            widget.destroy()
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            if recherche:
                cursor.execute("SELECT cni, nom, prenom, groupe_sanguin FROM patients WHERE nom LIKE ? OR cni LIKE ?",
                               (f'%{recherche}%', f'%{recherche}%'))
            else:
                cursor.execute("SELECT cni, nom, prenom, groupe_sanguin FROM patients")
            patients = cursor.fetchall()
            conn.close()

            if not patients:
                ctk.CTkLabel(self.liste_patients_frame, text="Aucun patient trouvé.", text_color="gray",
                             font=("Arial", 14, "italic")).pack(pady=20)
                return

            for p in patients:
                carte = ctk.CTkFrame(self.liste_patients_frame, fg_color="#FFFFFF", border_color="#A3C4BC",
                                     border_width=1)
                carte.pack(fill="x", pady=5, padx=10)
                info = f"👤 {p[1].upper()} {p[2].capitalize()}   |   💳 CNI: {p[0]}   |   🩸 Sang: {p[3]}"
                ctk.CTkLabel(carte, text=info, font=("Arial", 15, "bold"), text_color="#284A48").pack(side="left",
                                                                                                      padx=20, pady=15)
                ctk.CTkButton(carte, text="Ouvrir Dossier 🩺", width=120, fg_color="#284A48",
                              command=lambda pat=p: self.ouvrir_ordonnance_patient(pat)).pack(side="right", padx=20,
                                                                                              pady=15)
        except Exception as e:
            print(f"Erreur SQL : {e}")

    # --- 2. AJOUT PATIENT ---
    def afficher_formulaire_patient(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="🗂️ NOUVEAU DOSSIER PATIENT", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 10))
        form_frame = ctk.CTkFrame(self.zone_contenu, fg_color="transparent")
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        self.entry_cni = self.creer_champ_saisie(form_frame, "Numéro CNI (Unique) *")
        self.entry_nom = self.creer_champ_saisie(form_frame, "Nom *")
        self.entry_prenom = self.creer_champ_saisie(form_frame, "Prénom *")
        self.entry_date = self.creer_champ_saisie(form_frame, "Date de naissance (JJ/MM/AAAA)")
        self.entry_sang = self.creer_champ_saisie(form_frame, "Groupe Sanguin (ex: O+)")
        ctk.CTkLabel(form_frame, text="Antécédents Médicaux (Maladies, Allergies) :", font=("Arial", 12, "bold"),
                     text_color="#284A48").pack(anchor="w", pady=(10, 0))
        self.entry_antecedents = ctk.CTkTextbox(form_frame, height=80, fg_color="#A3C4BC", text_color="#284A48")
        self.entry_antecedents.pack(fill="x", pady=5)
        ctk.CTkButton(form_frame, text="💾 SAUVEGARDER LE PATIENT", font=("Arial", 14, "bold"), fg_color="#2C8D65",
                      hover_color="#1E5631", command=self.sauvegarder_patient).pack(pady=20, ipady=5)

    def creer_champ_saisie(self, parent, texte_placeholder):
        entry = ctk.CTkEntry(parent, placeholder_text=texte_placeholder, fg_color="#A3C4BC", text_color="#284A48")
        entry.pack(fill="x", pady=8)
        return entry

    def sauvegarder_patient(self):
        cni = self.entry_cni.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        date_n = self.entry_date.get()
        sang = self.entry_sang.get()
        antecedents = self.entry_antecedents.get("0.0", "end").strip()
        if not cni or not nom or not prenom:
            messagebox.showwarning("Erreur", "Veuillez remplir au moins le CNI, le Nom et le Prénom !")
            return
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, cni TEXT UNIQUE, nom TEXT, prenom TEXT, date_naissance TEXT, groupe_sanguin TEXT, antecedents_medicaux TEXT)''')
            cursor.execute(
                '''INSERT INTO patients (cni, nom, prenom, date_naissance, groupe_sanguin, antecedents_medicaux) VALUES (?, ?, ?, ?, ?, ?)''',
                (cni, nom, prenom, date_n, sang, antecedents))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès 🎉", f"Le patient {nom} {prenom} a été enregistré avec succès dans MedSafe !")
            self.afficher_malades()
        except sqlite3.IntegrityError:
            messagebox.showerror("Patient Existant", f"Un patient avec la CNI {cni} existe déjà dans le système !")

    # --- 3. JOURNAL MÉDICAL ---
    def afficher_journal(self):
        self.nettoyer_contenu()
        if not hasattr(self, 'patient_actuel'):
            ctk.CTkLabel(self.zone_contenu, text="⚠️ Veuillez d'abord sélectionner un patient dans 'Gestion Malades'",
                         font=("Arial", 16, "bold"), text_color="red").pack(pady=100)
            return
        p = self.patient_actuel
        header_patient = ctk.CTkFrame(self.zone_contenu, fg_color="#284A48", corner_radius=10)
        header_patient.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_patient, text=f"HISTORIQUE DE : {p[1].upper()} {p[2].capitalize()}   |   CNI : {p[0]}",
                     font=("Arial", 16, "bold"), text_color="#FAF9F6").pack(pady=15)

        form_frame = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        form_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(form_frame, text="Nouvelle Consultation :", font=("Arial", 14, "bold"), text_color="#284A48").pack(
            side="left", padx=10)
        self.entry_date_cons = ctk.CTkEntry(form_frame, placeholder_text="Date (ex: 29/04/2026)", width=150,
                                            fg_color="#FFFFFF", text_color="#284A48")
        self.entry_date_cons.pack(side="left", padx=10, pady=15)
        self.entry_diag = ctk.CTkEntry(form_frame, placeholder_text="Diagnostic (ex: Angine...)", width=250,
                                       fg_color="#FFFFFF", text_color="#284A48")
        self.entry_diag.pack(side="left", padx=10, pady=15)
        ctk.CTkButton(form_frame, text="💾 Enregistrer", fg_color="#2C8D65", command=self.sauvegarder_consultation).pack(
            side="right", padx=15)

        ctk.CTkLabel(self.zone_contenu, text="Consultations Précédentes :", font=("Arial", 14, "bold"),
                     text_color="#284A48").pack(anchor="w", padx=40, pady=(20, 5))
        self.liste_consultations = ctk.CTkScrollableFrame(self.zone_contenu, fg_color="#FFFFFF", border_color="#A3C4BC",
                                                          border_width=2)
        self.liste_consultations.pack(fill="both", expand=True, padx=40, pady=5)
        self.charger_historique_consultations()

    def sauvegarder_consultation(self):
        date_c = self.entry_date_cons.get()
        diag = self.entry_diag.get()
        if not date_c or not diag:
            messagebox.showwarning("Erreur", "Remplissez la date et le diagnostic !")
            return
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS consultations (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, date_consultation TEXT, diagnostic TEXT, observations TEXT)''')
            cursor.execute(
                '''INSERT INTO consultations (patient_id, date_consultation, diagnostic, observations) VALUES (?, ?, ?, ?)''',
                (self.patient_actuel[0], date_c, diag, ""))
            conn.commit()
            conn.close()
            self.afficher_journal()
        except Exception as e:
            print(f"Erreur SQL : {e}")

    def charger_historique_consultations(self):
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT date_consultation, diagnostic FROM consultations WHERE patient_id = ? ORDER BY id DESC",
                (self.patient_actuel[0],))
            consultations = cursor.fetchall()
            conn.close()
            if not consultations:
                ctk.CTkLabel(self.liste_consultations, text="Aucun historique pour ce patient.", text_color="gray",
                             font=("Arial", 14, "italic")).pack(pady=20)
                return
            for c in consultations:
                carte = ctk.CTkFrame(self.liste_consultations, fg_color="#FAF9F6", border_color="#A3C4BC",
                                     border_width=1)
                carte.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(carte, text=f"📅 {c[0]}   |   🩺 Diagnostic : {c[1]}", font=("Arial", 15, "bold"),
                             text_color="#284A48").pack(anchor="w", padx=20, pady=15)
        except Exception:
            pass

    # ---------------------------------------------------------
    # 4. LA ZONE ORDONNANCE (ÉDITEUR LIBRE EN TIMES NEW ROMAN 16)
    # ---------------------------------------------------------
    def ouvrir_ordonnance_patient(self, patient_data):
        self.patient_actuel = patient_data
        self.afficher_ordonnance()

    def afficher_ordonnance(self):
        self.nettoyer_contenu()

        if not hasattr(self, 'patient_actuel'):
            ctk.CTkLabel(self.zone_contenu,
                         text="⚠️ Veuillez d'abord sélectionner un patient dans 'Gestion Malades'",
                         font=("Arial", 16, "bold"), text_color="red").pack(pady=100)
            return

        p = self.patient_actuel

        header_patient = ctk.CTkFrame(self.zone_contenu, fg_color="#284A48", corner_radius=10)
        header_patient.pack(fill="x", padx=20, pady=20)

        infos = f"DOSSIER : {p[1].upper()} {p[2].capitalize()}   |   CNI : {p[0]}   |   GROUPE : {p[3]}"
        ctk.CTkLabel(header_patient, text=infos, font=("Arial", 16, "bold"), text_color="#FAF9F6").pack(pady=15)

        ctk.CTkLabel(self.zone_contenu, text="📝 RÉDACTION DE L'ORDONNANCE :", font=("Arial", 16, "bold"),
                     text_color="#284A48").pack(anchor="w", padx=40, pady=(10, 0))

        # La Grande Feuille Blanche, sans bouton d'analyse
        self.texte_ordonnance = ctk.CTkTextbox(self.zone_contenu, height=300, fg_color="#FFFFFF",
                                               border_color="#A3C4BC", border_width=2,
                                               font=("Times New Roman", 16), text_color="black")
        self.texte_ordonnance.pack(fill="both", expand=True, padx=40, pady=10)

        # En-tête Automatique du Médecin Connecté
        nom_med = self.medecin_info[1]
        spec_med = self.medecin_info[2]
        entete_ordonnance = f"Dr. {nom_med} - {spec_med}\n--------------------------------------------------------\n\nPrescription :\n\n- "

        self.texte_ordonnance.insert("0.0", entete_ordonnance)

        # Le seul bouton : l'exportation.
        ctk.CTkButton(self.zone_contenu, text="🖨️ EXPORTER L'ORDONNANCE (.txt)", fg_color="#2C8D65",
                      hover_color="#1E5631", width=250, height=40, font=("Arial", 14, "bold"),
                      command=self.exporter_ordonnance).pack(pady=20)

    def exporter_ordonnance(self):
        if not hasattr(self, 'patient_actuel'): return

        p = self.patient_actuel
        nom_patient = f"{p[1].upper()}_{p[2].capitalize()}"

        fichier_chemin = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"Ordonnance_{nom_patient}.txt",
            title="Enregistrer l'ordonnance",
            filetypes=[("Fichiers Texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )

        if fichier_chemin:
            try:
                contenu_ordonnance = self.texte_ordonnance.get("0.0", "end").strip()

                with open(fichier_chemin, 'w', encoding='utf-8') as fichier:
                    fichier.write("=" * 60 + "\n")
                    fichier.write("                 CABINET MÉDICAL MEDSAFE\n")
                    fichier.write("=" * 60 + "\n\n")
                    fichier.write(f"Patient(e) : {p[1].upper()} {p[2].capitalize()}\n")
                    fichier.write(f"CNI : {p[0]}   |   Groupe Sanguin : {p[3]}\n")
                    fichier.write("-" * 60 + "\n\n")
                    fichier.write(contenu_ordonnance + "\n\n")
                    fichier.write("=" * 60 + "\n")
                    fichier.write("Signature du médecin :\n")

                messagebox.showinfo("Succès 📄", f"L'ordonnance a été exportée avec succès !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'exporter le fichier : {e}")

    # ---------------------------------------------------------
    # 5. LA ZONE ÉQUIPEMENT (INVENTAIRE SQL - CRUD COMPLET)
    # ---------------------------------------------------------
    def afficher_equipement(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="🩺 GESTION DES ÉQUIPEMENTS", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        form_frame.pack(fill="x", padx=40, pady=10)

        self.entry_nom_eq = ctk.CTkEntry(form_frame, placeholder_text="Article (ex: Seringues)", width=200,
                                         fg_color="#FFFFFF", text_color="#284A48")
        self.entry_nom_eq.pack(side="left", padx=10, pady=15)

        self.entry_qte_eq = ctk.CTkEntry(form_frame, placeholder_text="Quantité (ex: 50)", width=120,
                                         fg_color="#FFFFFF", text_color="#284A48")
        self.entry_qte_eq.pack(side="left", padx=10, pady=15)

        self.entry_seuil_eq = ctk.CTkEntry(form_frame, placeholder_text="Seuil Alerte (ex: 10)", width=150,
                                           fg_color="#FFFFFF", text_color="#284A48")
        self.entry_seuil_eq.pack(side="left", padx=10, pady=15)

        ctk.CTkButton(form_frame, text="➕ Ajouter au Stock", fg_color="#2C8D65",
                      command=self.sauvegarder_equipement).pack(side="right", padx=15)

        self.liste_equipements = ctk.CTkScrollableFrame(self.zone_contenu, fg_color="#FFFFFF",
                                                        border_color="#A3C4BC", border_width=2)
        self.liste_equipements.pack(fill="both", expand=True, padx=40, pady=10)

        self.charger_equipements()

    def sauvegarder_equipement(self):
        nom = self.entry_nom_eq.get()
        qte = self.entry_qte_eq.get()
        seuil = self.entry_seuil_eq.get()

        if not nom or not qte:
            messagebox.showwarning("Erreur", "Veuillez remplir le nom et la quantité !")
            return

        try:
            seuil = int(seuil) if seuil else 5
            qte = int(qte)

            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO equipements (nom_article, quantite, seuil_alerte)
                              VALUES (?, ?, ?)''', (nom, qte, seuil))
            conn.commit()
            conn.close()
            self.afficher_equipement()
        except ValueError:
            messagebox.showerror("Erreur", "La quantité et le seuil doivent être des nombres entiers !")
        except Exception as e:
            print(f"Erreur SQL : {e}")

    def charger_equipements(self):
        for widget in self.liste_equipements.winfo_children(): widget.destroy()
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute("SELECT nom_article, quantite, seuil_alerte FROM equipements ORDER BY nom_article ASC")
            equipements = cursor.fetchall()
            conn.close()

            if not equipements:
                ctk.CTkLabel(self.liste_equipements, text="L'inventaire est vide.", text_color="gray",
                             font=("Arial", 14, "italic")).pack(pady=20)
                return

            for eq in equipements:
                nom, qte, seuil = eq

                if qte <= seuil:
                    couleur_fond = "#FFCDD2"
                    alerte_texte = "   ⚠️ RUPTURE IMMINENTE"
                else:
                    couleur_fond = "#FAF9F6"
                    alerte_texte = ""

                carte = ctk.CTkFrame(self.liste_equipements, fg_color=couleur_fond, border_color="#A3C4BC",
                                     border_width=1)
                carte.pack(fill="x", pady=5, padx=10)

                ctk.CTkLabel(carte, text=f"📦 {nom}   |   Quantité : {qte} (Seuil: {seuil}){alerte_texte}",
                             font=("Arial", 15, "bold"), text_color="#284A48").pack(side="left", padx=20, pady=15)

                btn_supprimer = ctk.CTkButton(carte, text="❌ Supprimer", width=100, fg_color="#D32F2F",
                                              hover_color="#B71C1C",
                                              command=lambda n=nom: self.supprimer_equipement(n))
                btn_supprimer.pack(side="right", padx=10, pady=15)

                btn_modifier = ctk.CTkButton(carte, text="✏️ Modifier", width=100, fg_color="#F57C00",
                                             hover_color="#E65100",
                                             command=lambda n=nom: self.modifier_equipement(n))
                btn_modifier.pack(side="right", padx=10, pady=15)

        except Exception as e:
            print(f"Erreur SQL : {e}")

    def supprimer_equipement(self, nom_article):
        reponse = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer '{nom_article}' du stock ?")
        if reponse:
            try:
                conn = sqlite3.connect('medsafe_cabinet.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM equipements WHERE nom_article = ?", (nom_article,))
                conn.commit()
                conn.close()
                self.afficher_equipement()
            except Exception as e:
                print(f"Erreur SQL : {e}")

    def modifier_equipement(self, nom_article):
        dialog = ctk.CTkInputDialog(text=f"Entrez la nouvelle quantité pour {nom_article} :", title="Modifier Stock")
        nouvelle_qte = dialog.get_input()

        if nouvelle_qte and nouvelle_qte.isdigit():
            try:
                conn = sqlite3.connect('medsafe_cabinet.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE equipements SET quantite = ? WHERE nom_article = ?",
                               (int(nouvelle_qte), nom_article))
                conn.commit()
                conn.close()
                self.afficher_equipement()
            except Exception as e:
                print(f"Erreur SQL : {e}")
        elif nouvelle_qte is not None:
            messagebox.showerror("Erreur", "La quantité doit être un chiffre exact !")


if __name__ == "__main__":
    login_app = LoginWindow()
    login_app.mainloop()

    if login_app.connexion_reussie:
        dashboard_app = DashboardMedecin(login_app.medecin_data)
        dashboard_app.mainloop()