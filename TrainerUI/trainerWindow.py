# trainerUI/trainerWindows.py
import customtkinter as ctk
import random
from MusicUtils.chords_analyser import ChordAnalyser
from MidiTools.midi_reader import MidiReader

class TrainerWindow:
    def __init__(self, root, _chord_dictionnary):
        self.root = root
        self.root.title("ChordTrainer - Trainer")
        self.root.attributes('-fullscreen', True)
        self.chord_dictionnary = _chord_dictionnary
        self.mode = "Chords"  # "Chords" ou "Song"
        self.midi_reader = MidiReader()  # Instance de MidiReader

        # Paramètres en dur pour le développement
        self.level = 1  # Niveau 1 pour les accords
        self.song_file = "./MySongs/test.sng"  # Fichier de chanson

        # Liste des accords à jouer
        self.chord_queue = []
        self.current_chord_index = 0  # Index de l'accord actuel
        self.played_chords = []  # Liste des résultats (True/False) pour les accords joués
        self.current_notes = []  # Notes MIDI actuellement jouées

        # Charger les accords selon le mode
        self.load_chords()

        # Configurer les zones horizontales
        self.setup_ui()

        # Lancer la lecture MIDI
        self.read_midi()

    def load_chords(self):
        if self.mode == "Chords":
            # Charger des accords aléatoires de niveau 1
            if self.level in self.chord_dictionnary.level:
                note_lists = self.chord_dictionnary.level[self.level]
                # Choisir 10 accords aléatoires (par exemple)
                self.chord_queue = [self.chord_dictionnary.content[note_list] for note_list in random.sample(note_lists, min(10, len(note_lists)))]
        else:  # mode == "Song"
            # Charger les accords depuis le fichier .sng
            with open(self.song_file, 'r') as f:
                chord_names = [line.strip() for line in f if line.strip()]
            # Convertir les noms d'accords en objets Chord
            for chord_name in chord_names:
                # Rechercher l'accord dans le dictionnaire
                for chord in self.chord_dictionnary.content.values():
                    if chord.shortname == chord_name:
                        self.chord_queue.append(chord)
                        break

    def setup_ui(self):
        # Calculer les hauteurs des zones
        screen_height = self.root.winfo_screenheight()
        zone_5_height = int(screen_height * 0.08)  # 8% pour le bouton de sortie
        remaining_height = screen_height - zone_5_height
        zone_height = remaining_height // 4  # 92% divisé en 4 zones égales

        # Zone 1 : File des accords
        self.zone1 = ctk.CTkFrame(master=self.root, height=zone_height)
        self.zone1.pack(fill="x", expand=False)
        self.zone1_labels = []  # Liste de labels pour les accords
        self.zone1_frame = ctk.CTkFrame(master=self.zone1)
        self.zone1_frame.pack(fill="both", expand=True)

        # Zone 2 : Formule des intervalles
        self.zone2 = ctk.CTkFrame(master=self.root, height=zone_height)
        self.zone2.pack(fill="x", expand=False)
        self.zone2_label = ctk.CTkLabel(
            master=self.zone2,
            text="",
            font=("Arial", 20),
            anchor="center"
        )
        self.zone2_label.pack(fill="both", expand=True)

        # Zone 3 : Diagramme de l'accord demandé
        self.zone3 = ctk.CTkFrame(master=self.root, height=zone_height)
        self.zone3.pack(fill="x", expand=False)
        self.zone3_label = ctk.CTkLabel(
            master=self.zone3,
            text="",
            font=("Keyboard Chord Diagram", 60),
            anchor="center"
        )
        self.zone3_label.pack(fill="both", expand=True)

        # Zone 4 : Diagramme de l'accord joué
        self.zone4 = ctk.CTkFrame(master=self.root, height=zone_height)
        self.zone4.pack(fill="x", expand=False)
        self.zone4_label = ctk.CTkLabel(
            master=self.zone4,
            text="",
            font=("Keyboard Chord Diagram", 60),
            anchor="center"
        )
        self.zone4_label.pack(fill="both", expand=True)

        # Zone 5 : Bouton de sortie
        self.zone5 = ctk.CTkFrame(master=self.root, height=zone_5_height)
        self.zone5.pack(fill="x", expand=False)
        self.exit_button = ctk.CTkButton(
            master=self.zone5,
            text="Retour",
            command=self.root.destroy,
            width=200,
            height=50,
            font=("Arial", 20),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.pack(pady=10)

        # Mettre à jour l'affichage initial
        self.update_display()

    def read_midi(self):
        # Vérifier les notes MIDI jouées
        notes = self.midi_reader.get_notes()
        if notes:
            for note, velocity in notes:
                if velocity > 0:  # Note On
                    if note not in self.current_notes:
                        self.current_notes.append(note)
                else:  # Note Off
                    if note in self.current_notes:
                        self.current_notes.remove(note)

            # Identifier l'accord joué
            if self.current_notes:
                played_chord = ChordAnalyser.analyse(self.current_notes, self.chord_dictionnary)
                if played_chord:
                    self.zone4_label.configure(text=played_chord.ChordDiagramString)

                    # Vérifier si l'accord joué correspond à l'accord demandé
                    if self.current_chord_index < len(self.chord_queue):
                        current_chord = self.chord_queue[self.current_chord_index]
                        if played_chord.noteList == current_chord.noteList:
                            self.played_chords.append(True)  # Accord correct
                            self.current_chord_index += 1
                            self.current_notes = []  # Réinitialiser les notes
                            self.update_display()
                        else:
                            self.played_chords.append(False)  # Accord incorrect
                            self.current_chord_index += 1
                            self.current_notes = []
                            self.update_display()

        # Relancer la lecture toutes les 100 ms
        self.root.after(100, self.read_midi)

    def update_display(self):
        # Zone 1 : Afficher la file des accords
        # Supprimer les anciens labels
        for label in self.zone1_labels:
            label.destroy()
        self.zone1_labels = []

        start_index = max(0, self.current_chord_index - 2)  # Commencer 2 accords avant
        end_index = min(len(self.chord_queue), self.current_chord_index + 3)  # Aller jusqu'à 2 accords après

        for i in range(start_index, end_index):
            chord = self.chord_queue[i]
            if i < self.current_chord_index:
                # Accord précédent : vert si bien joué, rouge sinon
                color = "green" if self.played_chords[i] else "red"
            elif i == self.current_chord_index:
                # Accord actuel : jaune
                color = "yellow"
            else:
                # Accords futurs : blanc
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
            self.zone3_label.configure(text=current_chord.ChordDiagramString)
        else:
            self.zone3_label.configure(text="")

        # Zone 4 : Afficher le diagramme de l'accord joué (mis à jour dans read_midi)
        if not self.current_notes:
            self.zone4_label.configure(text="")