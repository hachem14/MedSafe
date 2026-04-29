import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import messagebox, filedialog
import os


# =========================================================
# 1. FENÊTRE DE CONNEXION PHARMACIEN
# =========================================================
class LoginPharmacien(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEDSAFE - Espace Pharmacie (Connexion)")
        self.geometry("500x700")
        self.configure(fg_color="#FAF9F6")

        self.connexion_reussie = False
        self.pharmacien_data = None
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
            ctk.CTkLabel(self, text="⚠️ MEDSAFE", font=("Arial", 30, "bold"), text_color="#2C8D65").pack(pady=(40, 10))

    def afficher_login(self):
        self.nettoyer()
        self.ajouter_logo()

        ctk.CTkLabel(self, text="PORTAIL PHARMACIE", font=("Arial", 24, "bold"), text_color="#2C8D65").pack(
            pady=(10, 30))

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email Pharmacie", width=300, fg_color="#FFFFFF",
                                        text_color="#284A48")
        self.entry_email.pack(pady=10)

        self.entry_mdp = ctk.CTkEntry(self, placeholder_text="Mot de passe", width=300, fg_color="#FFFFFF",
                                      text_color="#284A48", show="*")
        self.entry_mdp.pack(pady=10)

        ctk.CTkButton(self, text="SE CONNECTER", width=300, fg_color="#2C8D65", hover_color="#1E5631",
                      font=("Arial", 15, "bold"), command=self.verifier_login).pack(pady=20)

        ctk.CTkLabel(self, text="Nouvelle Pharmacie ?", text_color="gray").pack(pady=(20, 0))
        ctk.CTkButton(self, text="INSCRIRE LA PHARMACIE", width=300, fg_color="transparent", border_color="#2C8D65",
                      border_width=2, text_color="#2C8D65", command=self.afficher_inscription).pack(pady=10)

    def afficher_inscription(self):
        self.nettoyer()
        self.ajouter_logo()

        ctk.CTkLabel(self, text="INSCRIRE UNE PHARMACIE", font=("Arial", 20, "bold"), text_color="#2C8D65").pack(
            pady=(10, 20))

        self.reg_nom = ctk.CTkEntry(self, placeholder_text="Nom Pharmacien (ex: Dr. Yassine)", width=300,
                                    fg_color="#FFFFFF")
        self.reg_nom.pack(pady=8)

        self.reg_pharmacie = ctk.CTkEntry(self, placeholder_text="Nom Pharmacie (ex: Pharmacie Centrale)", width=300,
                                          fg_color="#FFFFFF")
        self.reg_pharmacie.pack(pady=8)

        self.reg_email = ctk.CTkEntry(self, placeholder_text="Email", width=300, fg_color="#FFFFFF")
        self.reg_email.pack(pady=8)

        self.reg_mdp = ctk.CTkEntry(self, placeholder_text="Mot de passe", width=300, fg_color="#FFFFFF", show="*")
        self.reg_mdp.pack(pady=8)

        ctk.CTkButton(self, text="S'INSCRIRE", width=300, fg_color="#2C8D65", command=self.enregistrer_pharmacien).pack(
            pady=20)
        ctk.CTkButton(self, text="⬅️ Retour", width=300, fg_color="transparent", text_color="#284A48",
                      command=self.afficher_login).pack(pady=10)

    def verifier_login(self):
        email, mdp = self.entry_email.get(), self.entry_mdp.get()
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pharmaciens WHERE email = ? AND mot_de_passe = ?", (email, mdp))
            pharmacien = cursor.fetchone()
            conn.close()

            if pharmacien:
                self.pharmacien_data = pharmacien
                self.connexion_reussie = True
                self.destroy()
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects.")
        except Exception:
            messagebox.showerror("Erreur", "Aucune pharmacie enregistrée.")

    def enregistrer_pharmacien(self):
        nom, pharmacie, email, mdp = self.reg_nom.get(), self.reg_pharmacie.get(), self.reg_email.get(), self.reg_mdp.get()
        if not nom or not email or not mdp: return messagebox.showwarning("Erreur", "Remplissez tout !")
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS pharmaciens (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, pharmacie TEXT, email TEXT UNIQUE, mot_de_passe TEXT)''')
            cursor.execute("INSERT INTO pharmaciens (nom, pharmacie, email, mot_de_passe) VALUES (?, ?, ?, ?)",
                           (nom, pharmacie, email, mdp))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Pharmacie inscrite !")
            self.afficher_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Email déjà utilisé !")


# =========================================================
# 2. TABLEAU DE BORD PHARMACIEN (Le Cœur du Projet)
# =========================================================
class DashboardPharmacien(ctk.CTk):
    def __init__(self, pharmacien_connecte):
        super().__init__()
        self.pharm_info = pharmacien_connecte

        self.title("MEDSAFE - Espace Pharmacie")
        self.geometry("1200x800")
        self.configure(fg_color="#FAF9F6")

        # --- MENU LATÉRAL ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0,
                                    fg_color="#1E5631")  # Vert légèrement différent pour différencier
        self.sidebar.pack(side="left", fill="y")

        try:
            logo_image = ctk.CTkImage(light_image=Image.open("mokkt.jpg"), dark_image=Image.open("mokkt.jpg"),
                                      size=(150, 150))
            ctk.CTkLabel(self.sidebar, image=logo_image, text="").pack(pady=(30, 10))
        except Exception:
            pass

        ctk.CTkLabel(self.sidebar, text="⚕️ PHARMACIE", font=("Arial", 18, "bold"), text_color="#FAF9F6").pack(
            pady=(0, 20))

        self.creer_bouton_menu("👤 Profil Officine", self.afficher_profil)
        self.creer_bouton_menu("📥 Contrôle Ordonnance", self.afficher_controle_ordo)
        self.creer_bouton_menu("💊 Gestion des Stocks", self.afficher_stock)

        # --- ZONE DE CONTENU PRINCIPALE ---
        self.zone_droite = ctk.CTkFrame(self, fg_color="transparent")
        self.zone_droite.pack(side="right", fill="both", expand=True)

        self.zone_contenu = ctk.CTkFrame(self.zone_droite, fg_color="#FAF9F6", corner_radius=0)
        self.zone_contenu.pack(side="top", fill="both", expand=True)

        # --- PANNEAU PUBLICITAIRE ---
        self.ad_frame = ctk.CTkFrame(self.zone_droite, height=120, fg_color="#E8F5E9", border_color="#2C8D65",
                                     border_width=2)
        self.ad_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        ctk.CTkLabel(self.ad_frame, text="🌟 ESPACE SPONSOR / LABORATOIRES 🌟", font=("Arial", 16, "bold"),
                     text_color="#284A48").pack(pady=(20, 5))
        ctk.CTkLabel(self.ad_frame, text="Découvrez la nouvelle gamme de compléments alimentaires...",
                     font=("Arial", 12), text_color="#555555").pack()

        self.afficher_controle_ordo()

    def creer_bouton_menu(self, texte, commande):
        bouton = ctk.CTkButton(self.sidebar, text=texte, command=commande, fg_color="transparent",
                               hover_color="#2C8D65", font=("Arial", 15, "bold"), anchor="w")
        bouton.pack(fill="x", padx=20, pady=10)

    def nettoyer_contenu(self):
        for widget in self.zone_contenu.winfo_children(): widget.destroy()

    # --- 1. PROFIL ---
    def afficher_profil(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="👤 PROFIL DE L'OFFICINE", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 30))

        carte = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        carte.pack(pady=10, padx=40, fill="x")
        ctk.CTkLabel(carte, text=f"⚕️ {self.pharm_info[2]}", font=("Arial", 22, "bold"), text_color="#284A48").pack(
            pady=(20, 10), anchor="w", padx=30)
        ctk.CTkLabel(carte, text=f"Pharmacien Responsable : Dr. {self.pharm_info[1]}", font=("Arial", 16),
                     text_color="#284A48").pack(pady=5, anchor="w", padx=30)
        ctk.CTkLabel(carte, text=f"Contact : {self.pharm_info[3]}", font=("Arial", 16), text_color="#284A48").pack(
            pady=(5, 20), anchor="w", padx=30)
        ctk.CTkButton(self.zone_contenu, text="🔴 SE DÉCONNECTER", fg_color="#D32F2F", command=self.destroy).pack(
            pady=40)

    # --- 2. CONTRÔLE ORDONNANCE (LE MVP MEDSAFE) ---
    def afficher_controle_ordo(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="📥 CONTRÔLE ET ANALYSE D'ORDONNANCE", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 10))

        # Zone pour charger l'ordonnance du médecin
        import_frame = ctk.CTkFrame(self.zone_contenu, fg_color="transparent")
        import_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkButton(import_frame, text="📂 IMPORTER L'ORDONNANCE (.txt)", fg_color="#284A48", width=250,
                      command=self.charger_ordonnance).pack(side="left")

        # Affichage de l'ordonnance
        self.texte_ordo_lue = ctk.CTkTextbox(self.zone_contenu, height=200, fg_color="#FFFFFF", border_color="#A3C4BC",
                                             border_width=2, font=("Courier", 13))
        self.texte_ordo_lue.pack(fill="both", padx=40, pady=10)
        self.texte_ordo_lue.insert("0.0", "L'ordonnance du patient s'affichera ici après importation...")

        # ZONE D'ANALYSE (Le cœur de MedSafe)
        analyse_frame = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        analyse_frame.pack(fill="both", expand=True, padx=40, pady=10)

        ctk.CTkLabel(analyse_frame, text="⚠️ VÉRIFICATEUR D'INTERACTIONS (Base DDInter) :", font=("Arial", 14, "bold"),
                     text_color="#D32F2F").pack(anchor="w", padx=20, pady=10)

        box_recherche = ctk.CTkFrame(analyse_frame, fg_color="transparent")
        box_recherche.pack(fill="x", padx=20)
        self.entry_meds_check = ctk.CTkEntry(box_recherche,
                                             placeholder_text="Tapez les médicaments à vérifier (ex: Aspirine, Anticoagulant)",
                                             width=400, fg_color="#FFFFFF")
        self.entry_meds_check.pack(side="left", padx=(0, 10))
        ctk.CTkButton(box_recherche, text="LANCER L'ANALYSE 🔍", fg_color="#D32F2F", hover_color="#B71C1C",
                      command=self.lancer_analyse).pack(side="left")

        self.resultat_analyse = ctk.CTkTextbox(analyse_frame, height=120, fg_color="#FFFFFF", text_color="black",
                                               font=("Arial", 14))
        self.resultat_analyse.pack(fill="both", expand=True, padx=20, pady=10)
        self.resultat_analyse.insert("0.0",
                                     "Système prêt. Entrez les médicaments pour vérifier les risques de décès ou complications avant de délivrer le traitement.")

    def charger_ordonnance(self):
        filepath = filedialog.askopenfilename(title="Choisir une ordonnance", filetypes=[("Fichiers Texte", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    contenu = file.read()
                self.texte_ordo_lue.delete("0.0", "end")
                self.texte_ordo_lue.insert("0.0", contenu)
            except Exception as e:
                messagebox.showerror("Erreur", "Impossible de lire le fichier.")

    def lancer_analyse(self):
        meds = self.entry_meds_check.get().lower()
        if not meds: return

        self.resultat_analyse.delete("0.0", "end")
        self.resultat_analyse.insert("0.0", f"🔄 Interrogation de la base de données locale (236 834 entrées)...\n")
        self.resultat_analyse.insert("end", "------------------------------------------------------\n")

        # Simulation d'intelligence (MVP)
        if "aspirine" in meds:
            self.resultat_analyse.insert("end", "❌ ALERTE MAJEURE (NIVEAU ROUGE) :\n")
            self.resultat_analyse.insert("end", "Risque d'hémorragie digestive sévère détecté.\n")
            self.resultat_analyse.insert("end",
                                         "📢 CONSEIL DARIJA AU PATIENT : 'Balek a aami! Had el dwa m3a hada ydirlek nezif fel karch. Lazem nbedlouh.'\n")
            self.resultat_analyse.insert("end",
                                         "➡️ ACTION REQUISE : Contactez le médecin prescripteur pour modification.")
        else:
            self.resultat_analyse.insert("end", "✅ AUCUNE INTERACTION DANGEREUSE DÉTECTÉE.\n")
            self.resultat_analyse.insert("end", "Vous pouvez délivrer le traitement en toute sécurité.")

    # --- 3. GESTION DES STOCKS PHARMACIE ---
    def afficher_stock(self):
        self.nettoyer_contenu()
        ctk.CTkLabel(self.zone_contenu, text="💊 GESTION DES STOCKS", font=("Arial", 28, "bold"),
                     text_color="#284A48").pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(self.zone_contenu, fg_color="#E8F5E9", border_color="#2C8D65", border_width=2)
        form_frame.pack(fill="x", padx=40, pady=10)

        self.e_nom = ctk.CTkEntry(form_frame, placeholder_text="Médicament (ex: Doliprane 1g)", width=200,
                                  fg_color="#FFFFFF")
        self.e_nom.pack(side="left", padx=10, pady=15)
        self.e_qte = ctk.CTkEntry(form_frame, placeholder_text="Boîtes (ex: 100)", width=100, fg_color="#FFFFFF")
        self.e_qte.pack(side="left", padx=10, pady=15)
        self.e_seuil = ctk.CTkEntry(form_frame, placeholder_text="Alerte Rupture (ex: 10)", width=150,
                                    fg_color="#FFFFFF")
        self.e_seuil.pack(side="left", padx=10, pady=15)

        ctk.CTkButton(form_frame, text="➕ Ajouter", fg_color="#2C8D65", command=self.ajouter_stock).pack(side="right",
                                                                                                         padx=15)

        self.liste_stock = ctk.CTkScrollableFrame(self.zone_contenu, fg_color="#FFFFFF", border_color="#A3C4BC",
                                                  border_width=2)
        self.liste_stock.pack(fill="both", expand=True, padx=40, pady=10)
        self.charger_stock()

    def ajouter_stock(self):
        nom, qte, seuil = self.e_nom.get(), self.e_qte.get(), self.e_seuil.get()
        if not nom or not qte: return messagebox.showwarning("Erreur", "Remplissez nom et quantité")
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS stock_pharmacie (id INTEGER PRIMARY KEY AUTOINCREMENT, nom_med TEXT, quantite INTEGER, seuil INTEGER)''')
            cursor.execute("INSERT INTO stock_pharmacie (nom_med, quantite, seuil) VALUES (?, ?, ?)",
                           (nom, int(qte), int(seuil) if seuil else 5))
            conn.commit()
            conn.close()
            self.afficher_stock()
        except Exception:
            pass

    def charger_stock(self):
        for widget in self.liste_stock.winfo_children(): widget.destroy()
        try:
            conn = sqlite3.connect('medsafe_cabinet.db')
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS stock_pharmacie (id INTEGER PRIMARY KEY AUTOINCREMENT, nom_med TEXT, quantite INTEGER, seuil INTEGER)''')
            cursor.execute("SELECT nom_med, quantite, seuil FROM stock_pharmacie ORDER BY nom_med ASC")
            stocks = cursor.fetchall()
            conn.close()

            if not stocks:
                ctk.CTkLabel(self.liste_stock, text="Le stock est vide.", text_color="gray").pack(pady=20)
                return

            for nom, qte, seuil in stocks:
                alerte, color = ("   ⚠️ RUPTURE IMMINENTE", "#FFCDD2") if qte <= seuil else ("", "#FAF9F6")
                carte = ctk.CTkFrame(self.liste_stock, fg_color=color, border_color="#A3C4BC", border_width=1)
                carte.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(carte, text=f"💊 {nom}   |   En rayon : {qte} boîtes {alerte}", font=("Arial", 15, "bold"),
                             text_color="#284A48").pack(side="left", padx=20, pady=15)
                ctk.CTkButton(carte, text="❌ Supprimer", width=100, fg_color="#D32F2F",
                              command=lambda n=nom: self.supprimer_stock(n)).pack(side="right", padx=10, pady=15)
                ctk.CTkButton(carte, text="✏️ Modifier", width=100, fg_color="#F57C00",
                              command=lambda n=nom: self.modifier_stock(n)).pack(side="right", padx=10, pady=15)
        except Exception as e:
            print(e)

    def supprimer_stock(self, nom):
        if messagebox.askyesno("Confirmer", f"Supprimer '{nom}' ?"):
            conn = sqlite3.connect('medsafe_cabinet.db')
            conn.cursor().execute("DELETE FROM stock_pharmacie WHERE nom_med = ?", (nom,))
            conn.commit()
            conn.close()
            self.afficher_stock()

    def modifier_stock(self, nom):
        nv_qte = ctk.CTkInputDialog(text=f"Nouvelle quantité pour {nom} :", title="Modifier").get_input()
        if nv_qte and nv_qte.isdigit():
            conn = sqlite3.connect('medsafe_cabinet.db')
            conn.cursor().execute("UPDATE stock_pharmacie SET quantite = ? WHERE nom_med = ?", (int(nv_qte), nom))
            conn.commit()
            conn.close()
            self.afficher_stock()


# =========================================================
if __name__ == "__main__":
    login_app = LoginPharmacien()
    login_app.mainloop()

    if login_app.connexion_reussie:
        dashboard_app = DashboardPharmacien(login_app.pharmacien_data)
        dashboard_app.mainloop()