import pygame
import pygame.midi
import threading
import queue
import time
from collections import deque
from MidiTools.midi_player import MidiPlayer
from Chords.chords_analyser import ChordAnalyser

class MidiReader:
    def __init__(self, device_id):
        """Initialize MIDI reader and player."""
        pygame.init()
        pygame.midi.init()
        self.device_id = device_id
        self.running = False
        self.midi_input = None
        self.thread = None
        self.event_queue = queue.Queue()  # Queue to pass MIDI events to player
        self.player = MidiPlayer(self.event_queue)
        self.note_fifo = deque(maxlen=12)  # FIFO for last 12 completed notes
        self.active_notes = {}  # Tracks currently pressed notes with timestamps
        self.chords = []  # List of detected chords (optional history)
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
        while self.running:
            if self.midi_input.poll():
                midi_events = self.midi_input.read(10)
                for event in midi_events:
                    status, note, velocity, _ = event[0]
                    timestamp = event[1]

                    # Handle MIDI events
                    if status & 0xF0 == 0x90 and velocity > 0:  # Note On
                        self.event_queue.put(("note_on", note, velocity))
                        self.active_notes[note] = timestamp  # Track note with timestamp
                        self._check_for_chord(timestamp, SIMULTANEITY_THRESHOLD)

                    elif status & 0x80 or (status & 0xF0 == 0x90 and velocity == 0):  # Note Off
                        self.event_queue.put(("note_off", note, 0))
                        if note in self.active_notes:
                            # Add to FIFO only when note is fully played (ON -> OFF)
                            self.note_fifo.append(note)
                            print(f"Last 12 notes played: {list(self.note_fifo)}")
                            del self.active_notes[note]  # Remove from active notes

            time.sleep(0.01)

    def _check_for_chord(self, current_timestamp, threshold):
        """Detect if 3-9 notes are played quasi-simultaneously."""
        active_timestamps = list(self.active_notes.values())
        if len(active_timestamps) >= 3:  # At least 3 notes to consider a chord
            # Check if all active notes are within the threshold
            min_time = min(active_timestamps)
            max_time = max(active_timestamps)
            if max_time - min_time <= threshold and 3 <= len(self.active_notes) <= 9:
                chord = sorted(self.active_notes.keys())  # Sort for consistent display
                self.chords.append(chord)  # Keep history (optional)
                ChordAnalyser(chord)  # Create ChordAnalyser instance

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