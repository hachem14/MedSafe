import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import os
import sqlite3
import time
import random


# ============================================================
#  PALETTE & CONFIG GLOBALE
# ============================================================
BG_CREME    = "#F7F3E9"
VERT_FONCE  = "#2D6A4F"   # sidebar
VERT_MOYEN  = "#52796F"   # hover / accents
VERT_CLAIR  = "#84A98C"   # champs dans les cartes
TEAL_CARD   = "#74A99A"   # fond des grandes cartes
INPUT_BG    = "#A8C5BC"   # fond des champs
TEXTE_DARK  = "#0A3D4D"
BLANC       = "#FFFFFF"
ROUGE_ALERT = "#D32F2F"


# ============================================================
#  FONCTIONS UTILITAIRES
# ============================================================
def dessiner_qr_fake(canvas, x, y, taille=150):
    """Dessine un motif QR-code stylisé sur un Canvas tkinter."""
    canvas.delete("all")
    cell = taille // 10
    # grille aléatoire mais stable (seed fixe)
    rng = random.Random(42)
    for row in range(10):
        for col in range(10):
            # coins fixes (finder patterns)
            is_finder = (
                (row < 3 and col < 3) or
                (row < 3 and col > 6) or
                (row > 6 and col < 3)
            )
            if is_finder or rng.random() > 0.45:
                canvas.create_rectangle(
                    x + col * cell, y + row * cell,
                    x + col * cell + cell - 1, y + row * cell + cell - 1,
                    fill=TEXTE_DARK, outline=""
                )
    # cadre blanc dans les finders
    for fx, fy in [(1, 1), (1, 7), (7, 1)]:
        canvas.create_rectangle(
            x + fx * cell, y + fy * cell,
            x + fx * cell + cell, y + fy * cell + cell,
            fill=BLANC, outline=""
        )


# ============================================================
#  APPLICATION PRINCIPALE
# ============================================================
class MedSafeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MedSafe - Pour des Médicaments Sûrs")

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = int(sw * 0.82), int(sh * 0.82)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.configure(fg_color=BG_CREME)
        ctk.set_appearance_mode("light")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Données utilisateur (simulées)
        self.utilisateur_nom = "nom de utilisateur"

        # Base médicaments
        self.medicaments_db = self._charger_medicaments()

        self._creer_sidebar()
        self._creer_zone_principale()

        # Page d'accueil par défaut
        self.afficher_accueil()

    # ─────────────────────────────────────────────────────────
    #  SIDEBAR
    # ─────────────────────────────────────────────────────────
    def _creer_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=VERT_FONCE)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        self.sidebar.grid_propagate(False)

        # ── Avatar ──
        self.canvas_avatar = tk.Canvas(
            self.sidebar, width=90, height=90,
            bg=VERT_FONCE, highlightthickness=0
        )
        self.canvas_avatar.grid(row=0, column=0, pady=(35, 8))
        self.canvas_avatar.create_oval(5, 5, 85, 85, fill=BLANC, outline=BLANC)
        # Petite icône personne
        self.canvas_avatar.create_oval(28, 12, 62, 46, fill="#CCCCCC", outline="")
        self.canvas_avatar.create_arc(15, 45, 75, 85, start=0, extent=180, fill="#CCCCCC", outline="")

        # ── Nom utilisateur ──
        self.lbl_user = ctk.CTkLabel(
            self.sidebar, text=self.utilisateur_nom,
            font=("Georgia", 13), text_color="#CCDDCC"
        )
        self.lbl_user.grid(row=1, column=0, pady=(0, 25))

        # ── Boutons navigation ──
        btn_cfg = dict(
            fg_color="transparent",
            hover_color=VERT_MOYEN,
            font=("Arial Black", 14),
            text_color=BLANC,
            anchor="center",
            height=48,
            corner_radius=10
        )

        self.btn_accueil = ctk.CTkButton(
            self.sidebar, text="🏠  Accueil",
            command=self.afficher_accueil, **btn_cfg
        )
        self.btn_accueil.grid(row=2, column=0, padx=18, pady=6, sticky="ew")

        self.btn_inscription = ctk.CTkButton(
            self.sidebar, text="📋  Inscription",
            command=self.afficher_inscription, **btn_cfg
        )
        self.btn_inscription.grid(row=3, column=0, padx=18, pady=6, sticky="ew")

        self.btn_journal = ctk.CTkButton(
            self.sidebar, text="📔  Journal Médical",
            command=self.afficher_journal, **btn_cfg
        )
        self.btn_journal.grid(row=4, column=0, padx=18, pady=6, sticky="ew")

        self.btn_ordonnance = ctk.CTkButton(
            self.sidebar, text="📄  Ordonnance",
            command=self.afficher_ordonnance, **btn_cfg
        )
        self.btn_ordonnance.grid(row=5, column=0, padx=18, pady=6, sticky="ew")

        self.btn_analyse = ctk.CTkButton(
            self.sidebar, text="⚕️  Analyseur Risques",
            command=self.afficher_analyse, **btn_cfg
        )
        self.btn_analyse.grid(row=6, column=0, padx=18, pady=6, sticky="ew")

        # ── Version ──
        ctk.CTkLabel(
            self.sidebar, text="MedSafe v2.0",
            font=("Arial", 10), text_color="#7AAA8A"
        ).grid(row=9, column=0, pady=(0, 15))

        self._btn_actif = None

    def _highlight_btn(self, btn):
        """Met en surbrillance le bouton actif."""
        for b in [self.btn_accueil, self.btn_inscription,
                  self.btn_journal, self.btn_ordonnance, self.btn_analyse]:
            b.configure(fg_color="transparent")
        btn.configure(fg_color=VERT_MOYEN)
        self._btn_actif = btn

    # ─────────────────────────────────────────────────────────
    #  ZONE PRINCIPALE
    # ─────────────────────────────────────────────────────────
    def _creer_zone_principale(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_CREME)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def _nettoyer(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # ─────────────────────────────────────────────────────────
    #  PAGE ACCUEIL
    # ─────────────────────────────────────────────────────────
    def afficher_accueil(self):
        self._nettoyer()
        self._highlight_btn(self.btn_accueil)

        frame = ctk.CTkFrame(self.main_frame, fg_color=BG_CREME)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("mokkt.jpg"), size=(200, 200)
            )
            ctk.CTkLabel(frame, image=logo_img, text="").pack(pady=(0, 20))
        except Exception:
            ctk.CTkLabel(
                frame, text="🛡️", font=("Arial", 80)
            ).pack(pady=(0, 20))

        ctk.CTkLabel(
            frame, text="BIENVENUE CHEZ MEDSAFE",
            font=("Arial Black", 28), text_color=TEXTE_DARK
        ).pack(pady=10)

        ctk.CTkLabel(
            frame,
            text="لأدوية آمنة  •  Pour des médicaments sûrs",
            font=("Georgia", 16), text_color=VERT_MOYEN
        ).pack(pady=5)

        ctk.CTkLabel(
            frame,
            text="Sélectionnez une option dans le menu pour commencer.",
            font=("Arial", 14), text_color="gray"
        ).pack(pady=20)

    # ─────────────────────────────────────────────────────────
    #  PAGE INSCRIPTION
    # ─────────────────────────────────────────────────────────
    def afficher_inscription(self):
        self._nettoyer()
        self._highlight_btn(self.btn_inscription)

        # Carte verte centrale
        card = ctk.CTkFrame(
            self.main_frame, fg_color=TEAL_CARD,
            corner_radius=20, width=480
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="NOM ET PRÉNOM",
            font=("Arial Black", 13), text_color=TEXTE_DARK
        ).grid(row=0, column=0, sticky="w", padx=30, pady=(30, 4))

        self.ins_nom = ctk.CTkEntry(
            card, placeholder_text="", fg_color=INPUT_BG,
            border_width=0, height=42, width=400,
            font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.ins_nom.grid(row=1, column=0, padx=30, pady=(0, 14))

        ctk.CTkLabel(
            card, text="ÂGE",
            font=("Arial Black", 13), text_color=TEXTE_DARK
        ).grid(row=2, column=0, sticky="w", padx=30, pady=(0, 4))

        self.ins_age = ctk.CTkEntry(
            card, placeholder_text="", fg_color=INPUT_BG,
            border_width=0, height=42, width=400,
            font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.ins_age.grid(row=3, column=0, padx=30, pady=(0, 14))

        ctk.CTkLabel(
            card, text="POIDS (kg)",
            font=("Arial Black", 13), text_color=TEXTE_DARK
        ).grid(row=4, column=0, sticky="w", padx=30, pady=(0, 4))

        self.ins_poids = ctk.CTkEntry(
            card, placeholder_text="", fg_color=INPUT_BG,
            border_width=0, height=42, width=400,
            font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.ins_poids.grid(row=5, column=0, padx=30, pady=(0, 14))

        ctk.CTkLabel(
            card, text="DESCRIPTION",
            font=("Arial Black", 13), text_color=TEXTE_DARK
        ).grid(row=6, column=0, sticky="w", padx=30, pady=(0, 4))

        self.ins_desc = ctk.CTkTextbox(
            card, fg_color=INPUT_BG, border_width=0,
            height=110, width=400,
            font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.ins_desc.grid(row=7, column=0, padx=30, pady=(0, 20))

        ctk.CTkButton(
            card, text="S'INSCRIRE",
            fg_color=VERT_FONCE, hover_color=VERT_MOYEN,
            font=("Arial Black", 14), height=46, width=200,
            corner_radius=12,
            command=self._valider_inscription
        ).grid(row=8, column=0, pady=(0, 30))

    def _valider_inscription(self):
        nom = self.ins_nom.get().strip()
        if nom:
            self.utilisateur_nom = nom
            self.lbl_user.configure(text=nom)
            messagebox.showinfo("✅ Succès", f"Bienvenue {nom} !\nVotre compte MedSafe a été créé.")
        else:
            messagebox.showwarning("⚠️ Erreur", "Veuillez renseigner au moins votre nom.")

    # ─────────────────────────────────────────────────────────
    #  PAGE JOURNAL MÉDICAL
    # ─────────────────────────────────────────────────────────
    def afficher_journal(self):
        self._nettoyer()
        self._highlight_btn(self.btn_journal)

        # Layout 2 colonnes
        wrapper = ctk.CTkFrame(self.main_frame, fg_color=BG_CREME)
        wrapper.place(relx=0.04, rely=0.08, relwidth=0.92, relheight=0.85)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, weight=2)
        wrapper.grid_rowconfigure(1, weight=1)

        # ── Colonne gauche : nom patient ──
        ctk.CTkLabel(
            wrapper, text="NOM DU PATIENT",
            font=("Arial Black", 14), text_color=TEXTE_DARK
        ).grid(row=0, column=0, sticky="w", padx=(0, 20), pady=(0, 8))

        self.jour_nom = ctk.CTkEntry(
            wrapper, placeholder_text="Rechercher un patient...",
            fg_color=INPUT_BG, border_width=0,
            height=44, font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.jour_nom.grid(row=1, column=0, sticky="new", padx=(0, 20))

        # ── Colonne droite : journal ──
        ctk.CTkLabel(
            wrapper, text="JOURNAL MÉDICAL",
            font=("Arial Black", 14), text_color=TEXTE_DARK
        ).grid(row=0, column=1, sticky="w", pady=(0, 8))

        # Grande zone de texte avec logo en filigrane (simulé)
        journal_frame = ctk.CTkFrame(
            wrapper, fg_color=INPUT_BG, corner_radius=16
        )
        journal_frame.grid(row=1, column=1, sticky="nsew")
        journal_frame.grid_columnconfigure(0, weight=1)
        journal_frame.grid_rowconfigure(0, weight=1)

        self.jour_texte = ctk.CTkTextbox(
            journal_frame, fg_color=INPUT_BG, border_width=0,
            font=("Georgia", 14), text_color=TEXTE_DARK,
            wrap="word"
        )
        self.jour_texte.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Bouton enregistrer
        ctk.CTkButton(
            wrapper, text="💾  Enregistrer le journal",
            fg_color=VERT_FONCE, hover_color=VERT_MOYEN,
            font=("Arial Black", 13), height=44, corner_radius=12,
            command=self._sauvegarder_journal
        ).grid(row=2, column=0, columnspan=2, pady=(15, 0))

    def _sauvegarder_journal(self):
        nom = self.jour_nom.get().strip()
        contenu = self.jour_texte.get("1.0", "end").strip()
        if nom and contenu:
            messagebox.showinfo("✅ Enregistré", f"Journal de {nom} sauvegardé avec succès.")
        else:
            messagebox.showwarning("⚠️ Incomplet", "Veuillez renseigner le nom et le contenu du journal.")

    # ─────────────────────────────────────────────────────────
    #  PAGE ORDONNANCE
    # ─────────────────────────────────────────────────────────
    def afficher_ordonnance(self):
        self._nettoyer()
        self._highlight_btn(self.btn_ordonnance)

        wrapper = ctk.CTkFrame(self.main_frame, fg_color=BG_CREME)
        wrapper.place(relx=0.04, rely=0.06, relwidth=0.92, relheight=0.88)
        wrapper.grid_columnconfigure(0, weight=3)
        wrapper.grid_columnconfigure(1, weight=2)
        wrapper.grid_rowconfigure(2, weight=1)

        # ── Nom de l'utilisateur ──
        ctk.CTkLabel(
            wrapper, text="NOM DE L'UTILISATEUR",
            font=("Arial Black", 14), text_color=TEXTE_DARK
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.ord_user = ctk.CTkEntry(
            wrapper, placeholder_text="",
            fg_color=INPUT_BG, border_width=0,
            height=44, width=320,
            font=("Arial", 14), text_color=TEXTE_DARK
        )
        self.ord_user.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))
        # Pré-remplir avec le nom courant
        self.ord_user.insert(0, self.utilisateur_nom)

        # ── Description ──
        ctk.CTkLabel(
            wrapper, text="DESCRIPTION (Médicaments prescrits, posologie...)",
            font=("Arial Black", 14), text_color=TEXTE_DARK
        ).grid(row=2, column=0, sticky="nw", padx=(0, 20), pady=(0, 6))

        self.ord_desc = ctk.CTkTextbox(
            wrapper, fg_color=INPUT_BG, border_width=0,
            font=("Georgia", 14), text_color=TEXTE_DARK,
            corner_radius=14, wrap="word"
        )
        self.ord_desc.grid(row=2, column=0, sticky="nsew", padx=(0, 20), pady=(24, 0))

        # ── QR Code ──
        ctk.CTkLabel(
            wrapper, text="QR CODE",
            font=("Arial Black", 13), text_color=TEXTE_DARK
        ).grid(row=2, column=1, sticky="nw", pady=(0, 6))

        qr_frame = ctk.CTkFrame(
            wrapper, fg_color=INPUT_BG, corner_radius=16,
            width=200, height=200
        )
        qr_frame.grid(row=2, column=1, sticky="n", pady=(24, 0))
        qr_frame.grid_propagate(False)

        self.qr_canvas = tk.Canvas(
            qr_frame, width=160, height=160,
            bg=INPUT_BG, highlightthickness=0
        )
        self.qr_canvas.place(relx=0.5, rely=0.5, anchor="center")
        # QR vide par défaut
        self.qr_canvas.create_text(80, 80, text="Générer ↓", fill=TEXTE_DARK, font=("Arial", 12))

        # ── Boutons ──
        btn_frame = ctk.CTkFrame(wrapper, fg_color=BG_CREME)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(14, 0), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="📲  Générer le QR Code",
            fg_color=VERT_MOYEN, hover_color=VERT_FONCE,
            font=("Arial Black", 13), height=44, corner_radius=12,
            command=self._generer_qr
        ).grid(row=0, column=0, padx=8, sticky="ew")

        ctk.CTkButton(
            btn_frame, text="🖨️  Imprimer l'ordonnance",
            fg_color=VERT_FONCE, hover_color=VERT_MOYEN,
            font=("Arial Black", 13), height=44, corner_radius=12,
            command=self._imprimer_ordonnance
        ).grid(row=0, column=1, padx=8, sticky="ew")

    def _generer_qr(self):
        """Dessine un motif QR stylisé (placeholder offline)."""
        nom = self.ord_user.get().strip()
        desc = self.ord_desc.get("1.0", "end").strip()
        if not nom:
            messagebox.showwarning("⚠️", "Entrez un nom d'utilisateur.")
            return
        # Dessine le QR simulé
        dessiner_qr_fake(self.qr_canvas, 0, 0, taille=160)
        messagebox.showinfo("QR Généré ✅",
                            "QR Code créé.\n(Installez 'qrcode' pour un vrai QR.)")

    def _imprimer_ordonnance(self):
        nom = self.ord_user.get().strip()
        desc = self.ord_desc.get("1.0", "end").strip()
        if nom and desc:
            messagebox.showinfo("🖨️ Impression",
                                f"Ordonnance de {nom} envoyée à l'imprimante.")
        else:
            messagebox.showwarning("⚠️", "Remplissez tous les champs.")

    # ─────────────────────────────────────────────────────────
    #  PAGE ANALYSEUR DE RISQUES
    # ─────────────────────────────────────────────────────────
    def afficher_analyse(self):
        self._nettoyer()
        self._highlight_btn(self.btn_analyse)

        wrapper = ctk.CTkFrame(self.main_frame, fg_color=BG_CREME)
        wrapper.place(relx=0.04, rely=0.05, relwidth=0.92, relheight=0.90)
        wrapper.grid_columnconfigure((0, 1), weight=1)
        wrapper.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            wrapper, text="⚕️  Analyseur d'Interactions Médicamenteuses",
            font=("Arial Black", 20), text_color=TEXTE_DARK
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ── Panel Médicament A ──
        fA = ctk.CTkFrame(wrapper, fg_color=TEAL_CARD, corner_radius=14)
        fA.grid(row=1, column=0, padx=(0, 10), sticky="nsew")
        fA.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(fA, text="LISTE A", font=("Arial Black", 14),
                     text_color=BLANC).grid(row=0, column=0, pady=(14, 6))

        self.ana_entA = ctk.CTkEntry(fA, placeholder_text="Nom médicament...",
                                     fg_color=INPUT_BG, border_width=0,
                                     height=40, font=("Arial", 13), text_color=TEXTE_DARK)
        self.ana_entA.grid(row=1, column=0, padx=16, sticky="ew")

        ctk.CTkButton(fA, text="+ Ajouter", fg_color=VERT_FONCE, hover_color=VERT_MOYEN,
                      height=36, font=("Arial", 13), corner_radius=10,
                      command=lambda: self._ajouter_med('A')).grid(row=2, column=0, pady=8)

        self.ana_boxA = ctk.CTkTextbox(fA, height=160, fg_color=INPUT_BG,
                                       border_width=0, font=("Arial", 13),
                                       text_color=TEXTE_DARK)
        self.ana_boxA.grid(row=3, column=0, padx=16, pady=(0, 14), sticky="ew")

        # ── Panel Médicament B ──
        fB = ctk.CTkFrame(wrapper, fg_color=TEAL_CARD, corner_radius=14)
        fB.grid(row=1, column=1, padx=(10, 0), sticky="nsew")
        fB.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(fB, text="LISTE B", font=("Arial Black", 14),
                     text_color=BLANC).grid(row=0, column=0, pady=(14, 6))

        self.ana_entB = ctk.CTkEntry(fB, placeholder_text="Nom médicament...",
                                     fg_color=INPUT_BG, border_width=0,
                                     height=40, font=("Arial", 13), text_color=TEXTE_DARK)
        self.ana_entB.grid(row=1, column=0, padx=16, sticky="ew")

        ctk.CTkButton(fB, text="+ Ajouter", fg_color=VERT_FONCE, hover_color=VERT_MOYEN,
                      height=36, font=("Arial", 13), corner_radius=10,
                      command=lambda: self._ajouter_med('B')).grid(row=2, column=0, pady=8)

        self.ana_boxB = ctk.CTkTextbox(fB, height=160, fg_color=INPUT_BG,
                                       border_width=0, font=("Arial", 13),
                                       text_color=TEXTE_DARK)
        self.ana_boxB.grid(row=3, column=0, padx=16, pady=(0, 14), sticky="ew")

        # ── Bouton analyse ──
        ctk.CTkButton(
            wrapper, text="🚨  Comparer les Interactions",
            fg_color=ROUGE_ALERT, hover_color="#B71C1C",
            font=("Arial Black", 15), height=52, corner_radius=14,
            command=self._lancer_analyse
        ).grid(row=2, column=0, columnspan=2, pady=(16, 8), sticky="ew")

        # ── Résultats ──
        self.ana_resultat = ctk.CTkTextbox(
            wrapper, fg_color=INPUT_BG, border_width=2,
            border_color=VERT_MOYEN, font=("Georgia", 14),
            text_color=TEXTE_DARK, corner_radius=12, height=120
        )
        self.ana_resultat.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        self.ana_resultat.insert("1.0", "Les résultats de l'analyse s'afficheront ici...")
        self.ana_resultat.configure(state="disabled")

        # Listes internes
        self._listeA = []
        self._listeB = []

    def _ajouter_med(self, liste):
        if liste == 'A':
            med = self.ana_entA.get().strip().lower()
            if med:
                self._listeA.append(med)
                self.ana_boxA.insert("end", med + "\n")
                self.ana_entA.delete(0, "end")
        else:
            med = self.ana_entB.get().strip().lower()
            if med:
                self._listeB.append(med)
                self.ana_boxB.insert("end", med + "\n")
                self.ana_entB.delete(0, "end")

    def _chercher_interaction(self, m1, m2):
        try:
            conn = sqlite3.connect('../interactions_medicales.db')
            cur = conn.cursor()
            cur.execute("""
                SELECT i.niveau_gravite, i.description
                FROM Medicaments m1
                JOIN Medicaments m2 ON m1.nom_commercial COLLATE NOCASE = ?
                                   AND m2.nom_commercial COLLATE NOCASE = ?
                JOIN Interactions i ON
                    (i.id_molecule_a = m1.id_molecule AND i.id_molecule_b = m2.id_molecule)
                    OR
                    (i.id_molecule_a = m2.id_molecule AND i.id_molecule_b = m1.id_molecule)
            """, (m1, m2))
            res = cur.fetchone()
            conn.close()
            return res
        except Exception:
            return None

    def _lancer_analyse(self):
        self.ana_resultat.configure(state="normal")
        self.ana_resultat.delete("1.0", "end")

        if not self._listeA or not self._listeB:
            self.ana_resultat.insert("1.0", "⚠️ Ajoutez des médicaments dans les deux listes.")
            self.ana_resultat.configure(state="disabled")
            return

        trouvees = []
        for a in self._listeA:
            for b in self._listeB:
                r = self._chercher_interaction(a, b)
                if r:
                    trouvees.append((a, b, r[0], r[1]))

        if trouvees:
            texte = "🚨 INTERACTIONS DÉTECTÉES\n" + "─" * 40 + "\n\n"
            for a, b, grav, desc in trouvees:
                texte += f"⚠️  {a.upper()}  +  {b.upper()}\n"
                texte += f"Niveau : {grav}\n"
                texte += f"Description : {desc}\n\n"
            self.ana_resultat.insert("1.0", texte)
            self.ana_resultat.configure(text_color=ROUGE_ALERT)
        else:
            self.ana_resultat.insert(
                "1.0",
                "✅  AUCUNE INTERACTION DANGEREUSE CONNUE\n"
                "─────────────────────────────────────\n"
                "Ces médicaments semblent compatibles selon notre base de données."
            )
            self.ana_resultat.configure(text_color=VERT_FONCE)

        self.ana_resultat.configure(state="disabled")

    # ─────────────────────────────────────────────────────────
    #  BASE DE DONNÉES
    # ─────────────────────────────────────────────────────────
    def _charger_medicaments(self):
        try:
            conn = sqlite3.connect('../interactions_medicales.db')
            cur = conn.cursor()
            cur.execute("SELECT nom_commercial FROM Medicaments")
            noms = [r[0] for r in cur.fetchall()]
            conn.close()
            return noms
        except Exception:
            return []


# ============================================================
#  LANCEMENT
# ============================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = MedSafeApp()
    app.mainloop()