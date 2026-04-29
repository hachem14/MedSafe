import sqlite3

def initialiser_base_de_donnees():
    # 1. Création et connexion au fichier de la base de données
    conn = sqlite3.connect('medsafe_cabinet.db')
    cursor = conn.cursor()

    # 2. Création de la table MEDECIN (Profil et Connexion)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medecins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            specialite TEXT,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL
        )
    ''')

    # 3. Création de la table PATIENTS (Gestion des Malades)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cni TEXT UNIQUE NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            groupe_sanguin TEXT,
            antecedents_medicaux TEXT
        )
    ''')

    # 4. Création de la table JOURNAL MEDICAL (Consultations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            date_consultation TEXT NOT NULL,
            diagnostic TEXT,
            observations TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # 5. Création de la table EQUIPEMENTS (Gestion du stock cabinet)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_article TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            seuil_alerte INTEGER DEFAULT 5
        )
    ''')

    # Insertion d'un médecin de test (pour pouvoir se connecter plus tard)
    try:
        cursor.execute('''
            INSERT INTO medecins (nom, specialite, email, mot_de_passe) 
            VALUES ('Dr. Ahmed', 'Généraliste', 'admin@medsafe.dz', 'admin123')
        ''')
    except sqlite3.IntegrityError:
        pass # Le médecin de test existe déjà

    # Sauvegarde et fermeture
    conn.commit()
    conn.close()
    print("✅ SUCCÈS : La base de données 'medsafe_cabinet.db' a été créée avec toutes ses tables !")

if __name__ == "__main__":
    initialiser_base_de_donnees()