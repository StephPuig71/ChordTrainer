# Définition des noms des notes en notation anglaise
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Génération du dictionnaire pour un piano 88 touches (MIDI 21 à 108)
midi_to_note = {midi: notes[midi % 12] for midi in range(21, 109)}

# Affichage du dictionnaire
print(midi_to_note)
print(midi_to_note[35])