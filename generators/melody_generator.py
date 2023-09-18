import numpy as np
import io
from mido import MidiFile, MidiTrack, Message
from keras.models import load_model
import pretty_midi
from scipy.io import wavfile
import uuid
from ui import utility


def generate_music(model, duration, tempo, temperature):
    # Define the sequence length and the number of unique notes you want to generate
    sequence_length = 100
    # Adjust based on your MIDI range (typically 128 for a full MIDI range)
    unique_notes = 128

    # Load the trained model
    loaded_model = load_model(f'models/trained_models/{model}.keras')

    # Initialize the pattern with a random seed sequence of length sequence_length
    start = np.random.randint(0, unique_notes - 1)
    pattern = [start] * sequence_length
    generated_notes = []

    # Adjust the length of the generated melody
    for i in range(int(duration * tempo) * 5):
        x = np.reshape(pattern, (1, sequence_length, 1))
        x = x / float(unique_notes)
        prediction = loaded_model.predict(x, verbose=0)

        # Apply temperature for randomness control
        # temperature = 0.7  # Experiment with different values
        prediction = np.log(prediction) / temperature
        prediction = np.exp(prediction) / np.sum(np.exp(prediction))

        index = np.random.choice(range(unique_notes), p=prediction.ravel())
        generated_notes.append(index)
        pattern.append(index)
        pattern = pattern[1:]

    # Create a new MIDI file for the generated melody
    output_midi_file = MidiFile()
    output_track = MidiTrack()
    output_midi_file.tracks.append(output_track)

    for note in generated_notes:
        msg = Message('note_on', note=note, velocity=64, time=int(100/tempo))
        output_track.append(msg)

        msg = Message('note_off', note=note, velocity=64, time=int(100/tempo))
        output_track.append(msg)

    # return output_midi_file
    midi_file_name = f'generated_melodies/generated_melody_{uuid.uuid1()}.mid'
    utility.save_melody(midi_file_name, output_midi_file)

    midi_file = midi_file_name
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    audio_data = midi_data.fluidsynth()
    audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    )
    virtual_file = io.BytesIO()
    wavfile.write(virtual_file, 44100, audio_data)
    return virtual_file
