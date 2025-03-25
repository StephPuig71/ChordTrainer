import pygame
import pygame.midi
import threading
import queue
import time
from collections import deque
from MidiTools.midi_player import MidiPlayer
from MusicUtils.chords_analyser import ChordAnalyser





class MidiReader:
    def __init__(self, device_id):
        """Initialize MIDI reader and player."""
        pygame.init()
        pygame.midi.init()
        self.device_id = device_id
        self.running = False
        self.midi_input = None
        self.thread = None
        self.event_queue = queue.Queue()
        self.player = MidiPlayer(self.event_queue)
        self.note_fifo = deque(maxlen=12)
        self.active_notes = {}
        self.chords = []
        self.last_note_time = 0
        self.current_chord = None  # Stocke l'accord en cours
        self.start()

    def start(self):
        """Start MIDI reading in a separate thread."""
        if not pygame.midi.get_init():
            raise RuntimeError("Error: MIDI initialization failed.")
        if self.device_id >= pygame.midi.get_count():
            raise ValueError(f"Error: Invalid ID {self.device_id}.")
        
        self.midi_input = pygame.midi.Input(self.device_id)
        self.running = True
        self.thread = threading.Thread(target=self._read_midi, daemon=True)
        self.thread.start()
        device_name = pygame.midi.get_device_info(self.device_id)[1].decode()
        print(f"Listening for MIDI events on {device_name}...")

    def _read_midi(self):
        """Read MIDI events, manage FIFO and detect chords."""
        SIMULTANEITY_THRESHOLD = 200  # ms window for chord detection
        CHORD_STABILIZATION_DELAY = 0.3  # seconds to wait after last note
        while self.running:
            if self.midi_input.poll():
                midi_events = self.midi_input.read(10)
                for event in midi_events:
                    status, note, velocity, _ = event[0]
                    timestamp = event[1]

                    if status & 0xF0 == 0x90 and velocity > 0:  # Note On
                        self.event_queue.put(("note_on", note, velocity))
                        self.active_notes[note] = timestamp
                        self.last_note_time = time.time()

                    elif status & 0x80 or (status & 0xF0 == 0x90 and velocity == 0):  # Note Off
                        self.event_queue.put(("note_off", note, 0))
                        if note in self.active_notes:
                            self.note_fifo.append(note)
                            print(f"Last 12 notes played: {list(self.note_fifo)}")
                            del self.active_notes[note]
                            # Réinitialise l'accord en cours si toutes les notes sont relâchées
                            if not self.active_notes:
                                self.current_chord = None

            # Detect chord if stabilized and not yet detected
            current_time = time.time()
            current_size = len(self.active_notes)
            if (self.active_notes and 
                current_size >= 3 and 
                (current_time - self.last_note_time) > CHORD_STABILIZATION_DELAY and 
                self.current_chord is None):
                active_timestamps = list(self.active_notes.values())
                if max(active_timestamps) - min(active_timestamps) <= SIMULTANEITY_THRESHOLD:
                    keysList = sorted(self.active_notes.keys())
                    self.chords.append(keysList)
                    chord = ChordAnalyser.analyse(keysList, chord_dictionnary)
                    #self.current_chord = tuple(chord)  # Stocke comme tuple

            time.sleep(0.01)

    def stop(self):
        """Stop the MIDI reader and player."""
        self.running = False
        if self.thread:
            self.thread.join()
        if self.midi_input:
            self.midi_input.close()
        self.player.stop()
        pygame.midi.quit()
        pygame.quit()

    def __del__(self):
        """Ensure proper cleanup on object destruction."""
        self.stop()