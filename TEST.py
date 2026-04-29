import tkinter as tk
from tkinter import messagebox
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# 1. Chargement du modèle (Assure-toi que le dossier existe)
MODEL_PATH = "./reaction_model"
try:
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
    model.eval()  # Mode évaluation
except Exception as e:
    print(f"Erreur de chargement : {e}")


# 2. Fonction de prédiction
def tester_interaction():
    drug1 = entry_drug1.get().strip()
    drug2 = entry_drug2.get().strip()

    if not drug1 or not drug2:
        messagebox.showwarning("Attention", "Veuillez entrer le nom des deux médicaments.")
        return

    # Préparation de l'entrée selon le format d'entraînement
    input_text = f"react: {drug1} and {drug2}"

    try:
        # Tokenization et génération
        input_ids = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).input_ids
        with torch.no_grad():
            output = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)

        # Décodage du résultat
        prediction = tokenizer.decode(output[0], skip_special_tokens=True)

        # Affichage du résultat dans l'interface
        text_result.config(state=tk.NORMAL)
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, prediction)
        text_result.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")


# 3. Création de la fenêtre principale
root = tk.Tk()
root.title("Détecteur d'Interactions Médicamenteuses (DDI)")
root.geometry("500x400")
root.configure(padx=20, pady=20)

# Éléments visuels
tk.Label(root, text="Testeur de Modèle T5-DDI", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Médicament 1 :").pack(anchor="w")
entry_drug1 = tk.Entry(root, width=50)
entry_drug1.pack(pady=5)

tk.Label(root, text="Médicament 2 :").pack(anchor="w")
entry_drug2 = tk.Entry(root, width=50)
entry_drug2.pack(pady=5)

btn_predict = tk.Button(root, text="Prédire l'Interaction", command=tester_interaction, bg="#4CAF50", fg="white",
                        font=("Arial", 10, "bold"))
btn_predict.pack(pady=20)

tk.Label(root, text="Description de l'interaction :").pack(anchor="w")
text_result = tk.Text(root, height=5, width=50, state=tk.DISABLED, wrap=tk.WORD, bg="#f0f0f0")
text_result.pack(pady=5)

root.mainloop()