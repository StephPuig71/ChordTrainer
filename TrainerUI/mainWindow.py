# trainerUI/mainWindow.py
import customtkinter as ctk
from MusicUtils.chords_generator import ChordDictionnary, ChordDictionnaryGenerator
from .trainerWindow import TrainerWindow
from MidiTools.midi_reader import MidiReader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ChordTrainer")
        self.root.attributes('-fullscreen', True)  # Mode plein écran
        print("Initialisation de MainWindow")

        self.chord_dictionnary = ChordDictionnary()
        generator = ChordDictionnaryGenerator(self.chord_dictionnary)
        self.midi_reader = MidiReader(device_id=3)
        self.midi_reader.set_chord_dictionnary(self.chord_dictionnary)
        print("ChordDictionnary et MidiReader initialisés")


        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.chords_button = ctk.CTkButton(
            master=self.frame,
            text="Exercices d'accords",
            command=lambda: self.open_trainer("Chords"),
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.chords_button.pack(pady=10)

        self.song_button = ctk.CTkButton(
            master=self.frame,
            text="Travailler une chanson",
            command=lambda: self.open_trainer("Song"),
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.song_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(
            master=self.frame,
            text="Réglages",
            command=self.open_settings,
            width=300,
            height=50,
            font=("Arial", 20)
        )
        self.settings_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(
            master=self.frame,
            text="Exit",
            command=self.quit,
            width=300,
            height=50,
            font=("Arial", 20),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.pack(pady=10)

    def open_trainer(self, mode):
        trainer_window = ctk.CTkToplevel(self.root)
        trainer_window.attributes('-fullscreen', True)  # Mode plein écran
        print(f"Ouverture de TrainerWindow en mode {mode}")
        TrainerWindow(trainer_window, self.chord_dictionnary, mode, self.midi_reader)
        
            
    def open_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Réglages")
        settings_window.geometry("400x300")
        ctk.CTkLabel(settings_window, text="Fenêtre des réglages (à implémenter)").pack(pady=20)

    def quit(self):
        self.midi_reader.stop()
        self.root.quit()