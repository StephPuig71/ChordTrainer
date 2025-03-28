import threading
import time
import fluidsynth
import os
import queue

class MidiPlayer:
    def __init__(self, event_queue):
        """Initialize the MIDI player with a shared event queue."""
        self.event_queue = event_queue
        self.running = False
        self.thread = None
        self.fs = fluidsynth.Synth()
        soundfont_path = os.path.join(os.path.dirname(__file__), "FluidR3_GM.sf2")
        self.fs.start(driver="alsa")  # Use ALSA as audio driver
        self.sfid = self.fs.sfload(soundfont_path)
        self.fs.program_select(0, self.sfid, 0, 0)  # Select default instrument
        self.start()

    def start(self):
        """Start playing MIDI events in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._play_midi, daemon=True)
        self.thread.start()
        print("MIDI player started...")

    def _play_midi(self):
        """Process MIDI events from the queue and play them."""
        while self.running:
            try:
                event = self.event_queue.get(timeout=0.1)  # Wait for events
                event_type, note, velocity = event
                if event_type == "note_on":
                    self.fs.noteon(0, note, velocity)
                elif event_type == "note_off":
                    self.fs.noteoff(0, note)
                elif event_type == "control_change":
                    self.fs.cc(0, note, velocity)
                self.event_queue.task_done()
            except queue.Empty:
                time.sleep(0.01)  # Avoid busy waiting if queue is empty

    def stop(self):
        """Stop the MIDI player and clean up."""
        self.running = False
        if self.thread:
            self.thread.join()
        if hasattr(self, 'fs'):  # Vérifie que fs existe avant de le supprimer
            self.fs.delete()