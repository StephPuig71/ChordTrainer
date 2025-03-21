import time
from MidiTools.midi_reader import MidiReader

def main():
    lecteur = MidiReader(device_id=3)  # ID 3 pour KeyStep 32 entrée
    try:
        while True:
            time.sleep(1)  # Garde le main vivant sans surcharger
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
        lecteur.stop()

if __name__ == "__main__":
    main()