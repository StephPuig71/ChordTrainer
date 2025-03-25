# main.py
import os
import customtkinter as ctk
from TrainerUI.mainWindow import MainWindow
from MusicUtils.chords_generator import ChordDictionnary, ChordDictionnaryGenerator

def main():
    # Générer le dictionnaire des accords une seule fois
    chord_dictionnary = ChordDictionnary()
    generator = ChordDictionnaryGenerator(chord_dictionnary)
    
    # Définir ALSA_CONFIG_DIR si non défini
    if "ALSA_CONFIG_DIR" not in os.environ:
        os.environ["ALSA_CONFIG_DIR"] = "/usr/share/alsa"

    # Créer la fenêtre principale
    root = ctk.CTk()
    app = MainWindow(root, chord_dictionnary)
    root.mainloop()

if __name__ == "__main__":
    main()