class ChordSeedDefinition:
    """Définition de la graine d'accord, pour base de la génération"""
    def __init__(self, _name, _shortName, _level):
        self.name = _name          # Nom complet de l'accord (ex. "Major")
        self.shortName = _shortName  # Abréviation (ex. "m" pour Minor)
        self.level = _level        # Niveau de complexité (1 à 4)

class Chord:
    """Informations utiles pour un accord"""
    def __init__(self, _rootNote: str, _formula: tuple, _notesList: tuple, _name: str, _shortName: str, _level: int):  # Changé bytes en int
        self.rootnote = _rootNote    # Note fondamentale (ex. "C")
        self.formula = _formula      # Intervalles en demi-tons (ex. (0, 4, 7))
        self.noteList = _notesList   # Liste des notes triées (ex. ('C', 'E', 'G'))
        self.name = _name            # Nom complet (ex. "CMajor")
        self.shortname = _shortName  # Nom abrégé (ex. "C")
        self.level = _level          # Niveau hérité de la graine
        self.ChordDiagramString = self._generate_diagram_string()  # Nouvelle propriété

    def _generate_diagram_string(self):
        """Génère la chaîne de diagramme pour deux octaves."""
        base_string = "|wbwbw|wbwbwbw|wbwbw|wbwbwbw|"
        diagram = list(base_string)

        note_positions = {
            'C': (1, 15),
            'C#': (2, 16),
            'D': (3, 17),
            'D#': (4, 18),
            'E': (5, 19),
            'F': (7, 21),
            'F#': (8, 22),
            'G': (9, 23),
            'G#': (10, 24),
            'A': (11, 25),
            'A#': (12, 26),
            'B': (13, 27)
        }

        # Calculer les notes MIDI à partir de la fondamentale et de la formule
        root_idx = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"].index(self.rootnote)
        notes = [(root_idx + interval) % 12 for interval in self.formula]  # Positions MIDI des notes

        # Trier les notes par ordre MIDI croissant, en commençant par la fondamentale
        sorted_notes = sorted(notes)
        # Ajuster pour que la fondamentale soit la première dans l'ordre
        fundamental_idx = notes[0]  # La fondamentale est toujours la première dans self.formula (interval 0)
        if fundamental_idx in sorted_notes:
            idx = sorted_notes.index(fundamental_idx)
            sorted_notes = sorted_notes[idx:] + sorted_notes[:idx]  # Rotation pour commencer par la fondamentale

        # Déterminer si on déborde dans la 2e octave
        max_interval = max(self.formula)
        use_second_octave = max_interval > 11

        # Appliquer les touches appuyées
        crossed_fundamental = False  # Indique si on a dépassé la fondamentale dans l'ordre MIDI
        for note_idx in sorted_notes:
            note_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][note_idx]
            pos = note_positions[note_name]

            # Si on a dépassé la fondamentale dans l'ordre MIDI, passer à la 2e octave
            if note_idx < fundamental_idx and crossed_fundamental:
                diagram[pos[1]] = diagram[pos[1]].upper()  # Deuxième octave
            else:
                diagram[pos[0]] = diagram[pos[0]].upper()  # Première octave

            # Si on dépasse la fondamentale dans l'ordre MIDI, activer le drapeau
            if note_idx >= fundamental_idx:
                crossed_fundamental = True

        return "".join(diagram)

    def __str__(self):
        returnString = ""
        returnString += self.rootnote + ", "
        returnString += str(self.formula) + ", "
        returnString += str(self.noteList) + ", "
        returnString += self.name + ", "
        returnString += self.shortname + ", "
        returnString += str(self.level)
        returnString += self.ChordDiagramString  # Ajout pour vérification
        return returnString          # Ex. "C, (0, 4, 7), ('C', 'E', 'G'), CMajor, C, 1"

class ChordDictionnary:
    """Dictionnaire d'accords"""
    def __init__(self):
        self.content = {}  # Dictionnaire {notes: Chord}
        self.levels = {}    # Dictionnaire {niveau: [liste de clés _chord.noteList]}

    def append(self, _chord: Chord):
        # Ajouter l'accord dans self.content
        self.content[_chord.noteList] = _chord

        # Ajouter la clé _chord.noteList dans self.level selon le niveau de l'accord
        chord_level = _chord.level
        if chord_level not in self.levels:
            self.levels[chord_level] = []  # Initialiser la liste pour ce niveau si elle n'existe pas
        self.levels[chord_level].append(_chord.noteList)


class ChordDictionnaryGenerator:
    def __init__(self, _chordsDictionnary):  # Typo : devrait être _chordsDictionnary
        self.notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]  # Liste des 12 notes
        self.formulas = {  # Signatures des triades
        # Triades
        (0, 4, 7): ChordSeedDefinition("Major", "", 1),
        (0, 3, 7): ChordSeedDefinition("Minor", "m", 1),
        (0, 3, 6): ChordSeedDefinition("Diminished", "dim", 2),
        (0, 4, 8): ChordSeedDefinition("Augmented", "aug", 2),
        (0, 2, 7): ChordSeedDefinition("Sus2", "sus2", 3),
        (0, 5, 7): ChordSeedDefinition("Sus4", "sus4", 3),
        # Tétrades (Level 4)
        (0, 4, 7, 11): ChordSeedDefinition("Major 7", "maj7", 4),
        (0, 3, 7, 10): ChordSeedDefinition("Minor 7", "m7", 4),
        (0, 4, 7, 10): ChordSeedDefinition("Dominant 7", "7", 4),
        (0, 3, 6, 10): ChordSeedDefinition("Minor 7 Flat 5", "m7b5", 4),
        (0, 3, 6, 9): ChordSeedDefinition("Diminished 7", "dim7", 4),
        (0, 4, 7, 9): ChordSeedDefinition("Major 6", "6", 4),
        (0, 3, 7, 9): ChordSeedDefinition("Minor 6", "m6", 4),
        (0, 2, 7, 10): ChordSeedDefinition("Sus2 7", "sus2 7", 4),
        (0, 5, 7, 10): ChordSeedDefinition("Sus4 7", "sus4 7", 4),
        # Pentades (Level 5)
        (0, 4, 7, 11, 14): ChordSeedDefinition("Major 9", "maj9", 5),
        (0, 3, 7, 10, 14): ChordSeedDefinition("Minor 9", "m9", 5),
        (0, 4, 7, 10, 14): ChordSeedDefinition("Dominant 9", "9", 5),
        (0, 4, 7, 10, 13): ChordSeedDefinition("Dominant 7 Flat 9", "7b9", 5),
        (0, 4, 7, 10, 15): ChordSeedDefinition("Dominant 7 Sharp 9", "7#9", 5),
        (0, 3, 6, 10, 14): ChordSeedDefinition("Minor 9 Flat 5", "m9b5", 5),
        (0, 4, 7, 9, 14): ChordSeedDefinition("Major 6/9", "6/9", 5),

 
       }
        self.generate(_chordsDictionnary)

    def generate(self, _chordsDictionnary: ChordDictionnary):
        for note_index in range(len(self.notes)):  # Pour chaque fondamentale
            for formule in self.formulas.keys():   # Pour chaque signature
                notesList = []
                for interval in formule:           # Calcule les notes à partir des intervalles
                    notesList.append(self.notes[(note_index + interval) % 12])
                chord = Chord(
                    self.notes[note_index],        # Fondamentale
                    formule,                       # Formule
                    tuple(sorted(notesList)),      # Notes triées
                    self.notes[note_index] + self.formulas[formule].name,    # Nom complet
                    self.notes[note_index] + self.formulas[formule].shortName,  # Nom abrégé
                    self.formulas[formule].level   # Niveau
                )
                _chordsDictionnary.append(chord)    # Ajoute au dictionnaire

if __name__ == "__main__":
    chordDictionnary = ChordDictionnary()
    generator = ChordDictionnaryGenerator(chordDictionnary)
    for key in chordDictionnary.content.keys():
        print(key, chordDictionnary.content[key])  # Affiche chaque entrée