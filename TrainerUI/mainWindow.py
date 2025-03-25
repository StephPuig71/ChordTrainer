import customtkinter as ctk
from .trainerWindow import TrainerWindow

# Définir le thème et l'apparence de customtkinter
ctk.set_appearance_mode("dark")  # Options : "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Options : "blue", "green", "dark-blue"

class MainWindow:
    def __init__(self, root, _chord_dictionnary):
        self.root = root
        self.root.title("ChordTrainer")
        self.root.attributes('-fullscreen', True)  # Plein écran

        # Générer le dictionnaire des accords
        self.chord_dictionnary = _chord_dictionnary

        # Créer un frame pour centrer les boutons
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Bouton "Exercices d'accords"
        self.chords_button = ctk.CTkButton(
            master=self.frame,
            text="Exercices d'accords",
            command=lambda: self.open_trainer("Chords"),
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.chords_button.pack(pady=10)

        # Bouton "Travailler une chanson"
        self.song_button = ctk.CTkButton(
            master=self.frame,
            text="Travailler une chanson",
            command=lambda: self.open_trainer("Song"),
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.song_button.pack(pady=10)

        # Bouton "Réglages"
        self.settings_button = ctk.CTkButton(
            master=self.frame,
            text="Réglages",
            command=self.open_settings,
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.settings_button.pack(pady=10)

        # Bouton "Exit"
        self.exit_button = ctk.CTkButton(
            master=self.frame,
            text="Exit",
            command=self.root.quit,
            width=300,
            height=50,
            font=("Arial", 20),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.pack(pady=10)

    def open_trainer(self, mode):
        # Créer une nouvelle fenêtre pour le trainer
        trainer_window = ctk.CTkToplevel(self.root)
        trainer_window.attributes('-fullscreen', True)
        TrainerWindow(trainer_window, self.chord_dictionnary, mode)

    def open_settings(self):
        # Placeholder pour la fenêtre des réglages
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Réglages")
        settings_window.geometry("400x300")
        ctk.CTkLabel(settings_window, text="Fenêtre des réglages (à implémenter)").pack(pady=20)
