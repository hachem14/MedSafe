# 💊 MedSafe

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-1F6AA8?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Application desktop de gestion des médicaments et ordonnances**

*Gérez vos médicaments, suivez vos ordonnances et ne manquez plus jamais une prise.*

</div>

---

## 📋 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancement](#-lancement)
- [Structure du projet](#-structure-du-projet)
- [Captures d'écran](#-captures-décran)
- [Contribuer](#-contribuer)
- [Auteur](#-auteur)
- [Licence](#-licence)

---

## 🔍 Aperçu

**MedSafe** est une application desktop développée en Python avec CustomTkinter, conçue pour aider les patients et les professionnels de santé à gérer facilement les médicaments et les ordonnances. L'interface moderne et intuitive permet un suivi rigoureux des traitements en cours.

---

## ✨ Fonctionnalités

- 💊 **Gestion des médicaments** — Ajouter, modifier et supprimer des médicaments avec leurs informations détaillées (nom, dosage, fréquence, durée)
- 📋 **Suivi des ordonnances** — Enregistrer et consulter les ordonnances médicales
- 🔔 **Rappels de prise** — Système d'alertes pour ne jamais oublier une dose
- 📊 **Historique de traitement** — Visualiser l'historique complet des médicaments pris
- 🔐 **Gestion sécurisée** — Protection des données personnelles et médicales
- 🌙 **Mode sombre / clair** — Interface adaptable grâce à CustomTkinter

---

## 🛠 Technologies utilisées

| Technologie | Rôle |
|------------|------|
| **Python 3.10+** | Langage principal |
| **CustomTkinter** | Interface graphique moderne |
| **SQLite** | Base de données locale |
| **Pillow (PIL)** | Gestion des images |

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- [Python 3.10+](https://www.python.org/downloads/)
- `pip` (inclus avec Python)

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/hachem14/MedSafe.git
cd MedSafe
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

> Si le fichier `requirements.txt` n'existe pas encore, installez manuellement :
> ```bash
> pip install customtkinter pillow
> ```

---

## ▶️ Lancement

```bash
python main.py
```

---

## 📁 Structure du projet

```
MedSafe/
│
├── main.py                  # Point d'entrée de l'application
├── requirements.txt         # Dépendances Python
├── README.md
│
├── assets/                  # Images, icônes, ressources visuelles
│   └── ...
│
├── database/                # Gestion de la base de données SQLite
│   └── db.py
│
├── views/                   # Écrans / pages de l'application
│   ├── home.py
│   ├── medicaments.py
│   └── ordonnances.py
│
└── components/              # Composants UI réutilisables
    └── ...
```

> ⚠️ La structure ci-dessus est indicative. Elle peut varier selon l'organisation réelle du projet.

---

## 📸 Captures d'écran

> *Des captures d'écran seront ajoutées prochainement.*

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. **Forkez** le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. **Commitez** vos changements (`git commit -m 'feat: ajout de ma fonctionnalité'`)
4. **Poussez** vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une **Pull Request**

---

## 👤 Auteur

**hachem14**

- GitHub : [@hachem14](https://github.com/hachem14)

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">
  Fait avec ❤️ et Python
</div>
