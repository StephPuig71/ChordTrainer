# Définition des noms des notes en notation anglaise
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Génération du dictionnaire pour un piano 88 touches (MIDI 21 à 108)
midi_to_note = {midi: notes[midi % 12] for midi in range(21, 109)}

class Note:
    def __init__(self,_midiNumber) :
        self.noteName = midi_to_note [_midiNumber]

    def __str__(self):
        return self.noteName
