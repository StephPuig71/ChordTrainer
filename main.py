import os
import time
from MidiTools.midi_reader import MidiReader

def main():
    # Définir ALSA_CONFIG_DIR si non défini
    if "ALSA_CONFIG_DIR" not in os.environ:
        os.environ["ALSA_CONFIG_DIR"] = "/usr/share/alsa"
    
    lecteur = MidiReader(device_id=3)  # ID 3 pour KeyStep 32 entrée
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
        lecteur.stop()

if __name__ == "__main__":
    main()