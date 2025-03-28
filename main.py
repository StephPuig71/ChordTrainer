# main.py
import os
import customtkinter as ctk
from TrainerUI.mainWindow import MainWindow
from MusicUtils.chords_generator import ChordDictionnary, ChordDictionnaryGenerator
from MidiTools.midi_reader import MidiReader

def main():
    if "ALSA_CONFIG_DIR" not in os.environ:
        os.environ["ALSA_CONFIG_DIR"] = "/usr/share/alsa"
    root = ctk.CTk()
    root.geometry("800x600")  # Taille fenêtrée
    print("Lancement de MainWindow")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()