class ChordAnalyser:
    def __init__(self, chord):
        """Initialize with a list of MIDI notes and display it."""
        self.chord = chord
        print(f"Chord received: {self.chord}")