import customtkinter as ctk
import random
import time
import os
import csv
from datetime import datetime
from MusicUtils.chords_analyser import ChordAnalyser

class TrainerWindow:
    def __init__(self, root, chord_dictionnary, mode, midi_reader):
        self.root = root
        self.root.title("ChordTrainer - Trainer")
        self.root.attributes('-fullscreen', True)
        print("Initialisation de TrainerWindow")
        self.chord_dictionnary = chord_dictionnary
        self.mode = mode
        self.midi_reader = midi_reader
        self.midi_reader.set_chord_dictionnary(chord_dictionnary)

        self.level = 1
        self.song_file = "./MySongs/test.sng"
        self.chord_queue = []
        self.current_chord_index = 0
        self.played_chords = [0] * 10
        self.current_notes = []
        self.midi_reader_enabled = False
        # Ajout pour le chronométrage et le suivi
        self.start_time = None  # Temps de début pour l’accord actuel
        self.csv_file = "trainerHistory.csv"
        self.init_csv()

        self.load_chords()
        print(f"Accords chargés : {[chord.shortname for chord in self.chord_queue]}")
        self.setup_ui()
        self.update_midi_reader_enabled(True)
        print("UI configurée et MIDI activé")

    def init_csv(self):
        """Initialise le fichier CSV avec les entêtes si nécessaire."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'requested_chord', 'time_taken', 'has_error'])
            print(f"Fichier {self.csv_file} créé avec les entêtes.")

    def load_chords(self):
        if self.mode == "Chords":
            if self.level in self.chord_dictionnary.levels:
                note_lists = self.chord_dictionnary.levels[self.level]
                self.chord_queue = [self.chord_dictionnary.content[note_list] for note_list in random.sample(note_lists, min(10, len(note_lists)))]
        else:
            try:
                with open(self.song_file, 'r') as f:
                    chord_names = [line.strip() for line in f if line.strip()]
                for chord_name in chord_names:
                    found = False
                    for chord in self.chord_dictionnary.content.values():
                        if chord.shortname.lower() == chord_name.lower():
                            self.chord_queue.append(chord)
                            found = True
                            break
                    if not found:
                        print(f"Accord non trouvé : {chord_name}")
            except FileNotFoundError:
                print(f"Fichier {self.song_file} non trouvé")

    def setup_ui(self):
        print("Configuration de l'UI")
        screen_height = self.root.winfo_screenheight()
        zone_5_height = int(screen_height * 0.08)
        zone_height = (screen_height - zone_5_height) // 4

        diagram_font_size = int(zone_height * 0.4)
        text_font_size = int(zone_height * 0.15)

        try:
            self.keyboard_font = ctk.CTkFont(family="Keyboard Chord Diagram", size=diagram_font_size)
            print("Police 'Keyboard Chord Diagram' chargée avec succès")
        except Exception as e:
            print(f"Erreur lors du chargement de la police 'Keyboard Chord Diagram' : {e}")
            self.keyboard_font = ctk.CTkFont(family="Arial", size=diagram_font_size)
            print("Utilisation de la police par défaut 'Arial'")

        self.text_font = ctk.CTkFont(family="Arial", size=text_font_size)

        self.zone1 = ctk.CTkFrame(master=self.root, fg_color="gray20")
        self.zone1.pack(fill="both", expand=True)
        self.zone1_labels = []
        self.zone1_frame = ctk.CTkFrame(master=self.zone1, fg_color="gray20")
        self.zone1_frame.pack(fill="both", expand=True)

        self.zone2 = ctk.CTkFrame(master=self.root, fg_color="gray30")
        self.zone2.pack(fill="both", expand=True)
        self.zone2_label = ctk.CTkLabel(
            master=self.zone2, text="", font=self.text_font, anchor="center", text_color="white"
        )
        self.zone2_label.pack(fill="both", expand=True)

        self.zone3 = ctk.CTkFrame(master=self.root, fg_color="gray40")
        self.zone3.pack(fill="both", expand=True)
        self.zone3_label = ctk.CTkLabel(
            master=self.zone3, text="", font=self.keyboard_font, anchor="center", text_color="white"
        )
        self.zone3_label.pack(fill="both", expand=True)

        self.zone4 = ctk.CTkFrame(master=self.root, fg_color="gray50")
        self.zone4.pack(fill="both", expand=True)
        self.zone4_label = ctk.CTkLabel(
            master=self.zone4, text="", font=self.keyboard_font, anchor="center", text_color="white"
        )
        self.zone4_label.pack(fill="both", expand=True)

        self.zone5 = ctk.CTkFrame(master=self.root, height=zone_5_height, fg_color="gray60")
        self.zone5.pack(fill="x", expand=False)
        self.exit_button = ctk.CTkButton(
            master=self.zone5, text="Retour", command=self.close, width=200, height=50,
            font=self.text_font, fg_color="red", hover_color="darkred"
        )
        self.exit_button.pack(pady=10)

        self.update_display()
        self.root.update()
        print("UI mise à jour")

    def close(self):
        self.update_midi_reader_enabled(False)
        self.root.destroy()

    def update_midi_reader_enabled(self, enabled):
        self.midi_reader_enabled = enabled
        if enabled:
            self.update_midi_reader()

    def update_midi_reader(self):
        if not self.midi_reader_enabled:
            return
        self.current_notes = list(self.midi_reader.active_notes.keys())
        if self.midi_reader.current_chord:
            played_chord = self.midi_reader.current_chord
            print(f"Affichage de l'accord joué : {played_chord.ChordDiagramString}")
            self.zone4_label.configure(text=played_chord.ChordDiagramString)
            self.zone4_label.update()
            if self.current_chord_index < len(self.chord_queue):
                current_chord = self.chord_queue[self.current_chord_index]
                if played_chord.noteList == current_chord.noteList:
                    # Calculer le temps écoulé
                    end_time = time.time()
                    time_taken = int((end_time - self.start_time) * 10)  # En dixièmes de seconde
                    has_error = "True" if self.played_chords[self.current_chord_index] == -1 else "False"
                    # Écrire dans le CSV
                    self.log_to_csv(current_chord.shortname, time_taken, has_error)
                    # Mettre à jour l’état
                    if self.played_chords[self.current_chord_index] != -1:
                        self.played_chords[self.current_chord_index] = 1
                    self.current_chord_index += 1
                    self.current_notes = []
                    self.midi_reader.current_chord = None
                    self.update_display()
                else:
                    self.played_chords[self.current_chord_index] = -1
        self.root.after(100, self.update_midi_reader)

    def log_to_csv(self, requested_chord, time_taken, has_error):
        """Écrit une ligne dans le fichier CSV."""
        # Horodatage au format AAAAMMJJhhmmss.d
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S") + f".{int(now.microsecond / 100000)}"
        # Écrire dans le CSV
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, requested_chord, time_taken, has_error])
        print(f"Progression enregistrée : {timestamp}, {requested_chord}, {time_taken}, {has_error}")

    def update_display(self):
        for label in self.zone1_labels:
            label.destroy()
        self.zone1_labels = []

        if not self.chord_queue:
            label = ctk.CTkLabel(
                master=self.zone1_frame,
                text="Aucun accord chargé",
                font=self.text_font,
                text_color="red",
                anchor="center"
            )
            label.pack(side="left", padx=20)
            self.zone1_labels.append(label)
            return

        start_index = max(0, self.current_chord_index - 2)
        end_index = min(len(self.chord_queue), self.current_chord_index + 3)

        for i in range(start_index, end_index):
            chord = self.chord_queue[i]
            if i < self.current_chord_index:
                if self.played_chords[i] == 1:
                    color = "green"
                elif self.played_chords[i] == -1:
                    color = "red"
                else:
                    color = "white"
            elif i == self.current_chord_index:
                color = "yellow"
            else:
                color = "white"

            label = ctk.CTkLabel(
                master=self.zone1_frame,
                text=chord.shortname,
                font=self.text_font,
                text_color=color,
                width=100,
                anchor="center"
            )
            label.pack(side="left", padx=20)
            self.zone1_labels.append(label)

        if self.current_chord_index < len(self.chord_queue):
            current_chord = self.chord_queue[self.current_chord_index]
            self.zone2_label.configure(text=f"Formule : {current_chord.formula}")
            self.zone2_label.update()
            print(f"Affichage de l'accord demandé : {current_chord.ChordDiagramString}")
            self.zone3_label.configure(text=current_chord.ChordDiagramString)
            self.zone3_label.update()
            # Démarrer le chronomètre pour cet accord
            self.start_time = time.time()
        else:
            self.zone2_label.configure(text="Exercice terminé")
            self.zone2_label.update()
            self.zone3_label.configure(text="")
            self.zone3_label.update()

        if not self.current_notes:
            self.zone4_label.configure(text="")
            self.zone4_label.update()