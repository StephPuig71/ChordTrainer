# trainerUI/trainerWindows.py
import customtkinter as ctk
import random
import tkinter.font as tkfont
from MusicUtils.chords_analyser import ChordAnalyser

class TrainerWindow:
    def __init__(self, root, chord_dictionnary, mode, midi_reader):
        self.root = root
        self.root.title("ChordTrainer - Trainer")
        self.root.attributes('-fullscreen', True)
        self.chord_dictionnary = chord_dictionnary
        self.mode = mode
        self.midi_reader = midi_reader

        # Paramètres en dur pour le développement
        self.level = 1
        self.song_file = "./MySongs/test.sng"

        # Liste des accords à jouer
        self.chord_queue = []
        self.current_chord_index = 0
        self.played_chords = []
        self.current_notes = []
        self.midi_reader_enabled = False

        # Charger les accords
        self.load_chords()
        print(f"Accords chargés : {[chord.shortname for chord in self.chord_queue]}")

        # Configurer les zones horizontales
        self.setup_ui()

        # Lancer la lecture MIDI
        self.update_midi_reader_enabled(True)

    def load_chords(self):
        if self.mode == "Chords":
            if self.level in self.chord_dictionnary.level:
                note_lists = self.chord_dictionnary.level[self.level]
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
        # Charger la police dynamiquement
        self.keyboard_font = tkfont.Font(file="./Keyboard Chord Diagram.ttf", size=60)

        # Calculer les hauteurs des zones
        screen_height = self.root.winfo_screenheight()
        zone_5_height = int(screen_height * 0.08)
        remaining_height = screen_height - zone_5_height
        zone_height = remaining_height // 4

        # Zone 1 : File des accords
        self.zone1 = ctk.CTkFrame(master=self.root, height=zone_height, fg_color="gray20")
        self.zone1.pack(fill="x", expand=False)
        self.zone1_labels = []
        self.zone1_frame = ctk.CTkFrame(master=self.zone1, fg_color="gray20")
        self.zone1_frame.pack(fill="both", expand=True)

        # Zone 2 : Formule des intervalles
        self.zone2 = ctk.CTkFrame(master=self.root, height=zone_height, fg_color="gray30")
        self.zone2.pack(fill="x", expand=False)
        self.zone2_label = ctk.CTkLabel(
            master=self.zone2,
            text="",
            font=("Arial", 20),
            anchor="center",
            text_color="white"
        )
        self.zone2_label.pack(fill="both", expand=True)

        # Zone 3 : Diagramme de l'accord demandé
        self.zone3 = ctk.CTkFrame(master=self.root, height=zone_height, fg_color="gray40")
        self.zone3.pack(fill="x", expand=False)
        self.zone3_label = ctk.CTkLabel(
            master=self.zone3,
            text="",
            font=self.keyboard_font,
            anchor="center",
            text_color="white"
        )
        self.zone3_label.pack(fill="both", expand=True)

        # Zone 4 : Diagramme de l'accord joué
        self.zone4 = ctk.CTkFrame(master=self.root, height=zone_height, fg_color="gray50")
        self.zone4.pack(fill="x", expand=False)
        self.zone4_label = ctk.CTkLabel(
            master=self.zone4,
            text="",
            font=self.keyboard_font,
            anchor="center",
            text_color="white"
        )
        self.zone4_label.pack(fill="both", expand=True)

        # Zone 5 : Bouton de sortie
        self.zone5 = ctk.CTkFrame(master=self.root, height=zone_5_height, fg_color="gray60")
        self.zone5.pack(fill="x", expand=False)
        self.exit_button = ctk.CTkButton(
            master=self.zone5,
            text="Retour",
            command=self.close,
            width=200,
            height=50,
            font=("Arial", 20),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.pack(pady=10)

        # Mettre à jour l'affichage initial
        self.update_display()

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

        # Utiliser self.midi_reader.active_notes pour les notes actuellement jouées
        self.current_notes = list(self.midi_reader.active_notes.keys())

        # Utiliser self.midi_reader.chords pour les accords détectés
        if self.midi_reader.chords:
            # Prendre le dernier accord détecté
            latest_chord_notes = self.midi_reader.chords[-1]
            played_chord = ChordAnalyser.analyse(latest_chord_notes, self.chord_dictionnary)
            if played_chord:
                self.zone4_label.configure(text=played_chord.ChordDiagramString)

                if self.current_chord_index < len(self.chord_queue):
                    current_chord = self.chord_queue[self.current_chord_index]
                    if played_chord.noteList == current_chord.noteList:
                        self.played_chords.append(True)
                        self.current_chord_index += 1
                        self.current_notes = []
                        self.midi_reader.chords.clear()  # Réinitialiser pour éviter les redétections
                        self.update_display()

        self.root.after(100, self.update_midi_reader)

    def update_display(self):
        # Zone 1 : Afficher la file des accords
        for label in self.zone1_labels:
            label.destroy()
        self.zone1_labels = []

        if not self.chord_queue:
            label = ctk.CTkLabel(
                master=self.zone1_frame,
                text="Aucun accord chargé",
                font=("Arial", 30),
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
                color = "green" if self.played_chords[i] else "red"
            elif i == self.current_chord_index:
                color = "yellow"
            else:
                color = "white"

            label = ctk.CTkLabel(
                master=self.zone1_frame,
                text=chord.shortname,
                font=("Arial", 30),
                text_color=color,
                width=100,
                anchor="center"
            )
            label.pack(side="left", padx=20)
            self.zone1_labels.append(label)

        # Zone 2 : Afficher la formule de l'accord actuel
        if self.current_chord_index < len(self.chord_queue):
            current_chord = self.chord_queue[self.current_chord_index]
            self.zone2_label.configure(text=f"Formule : {current_chord.formula}")
        else:
            self.zone2_label.configure(text="Exercice terminé")

        # Zone 3 : Afficher le diagramme de l'accord demandé
        if self.current_chord_index < len(self.chord_queue):
            current_chord = self.chord_queue[self.current_chord_index]
            self.zone3_label.configure(text=current_chord.ChordDiagramString)
            # Jouer l'accord demandé via event_queue
            self.play_chord(current_chord)
        else:
            self.zone3_label.configure(text="")

        # Zone 4 : Afficher le diagramme de l'accord joué
        if not self.current_notes:
            self.zone4_label.configure(text="")

    def play_chord(self, chord):
        # Convertir les notes de l'accord en valeurs MIDI
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        root_note = note_names.index(chord.rootnote) + 60  # MIDI note pour C4 = 60
        intervals = chord.formula
        midi_notes = [root_note + interval for interval in intervals]

        # Envoyer les événements à event_queue
        for note in midi_notes:
            self.midi_reader.event_queue.put(("note_on", note, 64))
        self.root.after(1000, lambda: self.stop_chord(midi_notes))

    def stop_chord(self, midi_notes):
        for note in midi_notes:
            self.midi_reader.event_queue.put(("note_off", note, 0))