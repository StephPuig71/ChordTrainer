# main.py
import os
import customtkinter as ctk
from TrainerUI.mainWindow import MainWindow
from MusicUtils.chords_generator import ChordDictionnary, ChordDictionnaryGenerator

def main():
    # Définir ALSA_CONFIG_DIR si non défini
    if "ALSA_CONFIG_DIR" not in os.environ:
        os.environ["ALSA_CONFIG_DIR"] = "/usr/share/alsa"

    # Créer la fenêtre principale
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()