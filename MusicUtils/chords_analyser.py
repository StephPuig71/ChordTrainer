# chords_analyser.py
from .notes_analyser import Note

class ChordAnalyser:
    @staticmethod
    def analyse(chord, chord_dictionnary):
        """
        Analyse une liste de notes MIDI et retourne l'accord correspondant.
        
        Args:
            chord (list): Liste de notes MIDI (ex. [60, 64, 67] pour C4, E4, G4).
            chord_dictionnary (ChordDictionnary): Dictionnaire des accords pour la recherche.
        
        Returns:
            Chord: L'objet Chord correspondant, ou None si aucun accord n'est trouvé.
        """
        print(f"Notes MIDI : {chord}")

        # Utiliser un set pour éliminer les doublons de noms de notes
        unique_note_names = set()
        for note in chord:
            note_name = Note(note).noteName  # Convertir la note MIDI en nom (ex. 60 → "C")
            unique_note_names.add(note_name)
        notes_list = list(unique_note_names)
        #print(f"Notes détectées (non triées) : {notes_list}")

        # Trier les notes pour correspondre à la clé du dictionnaire
        sorted_notes = tuple(sorted(notes_list))  # Convertir en tuple trié
        #print(f"Notes triées pour recherche : {sorted_notes}")

        # Rechercher l'accord dans le dictionnaire
        if sorted_notes in chord_dictionnary.content:
            matching_chord = chord_dictionnary.content[sorted_notes]
            print(f"Accord trouvé : {matching_chord}")
            return matching_chord
        else:
            print(f"Aucun accord trouvé pour les notes : {sorted_notes}")
            return None