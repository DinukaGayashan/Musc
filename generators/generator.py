import numpy as np
import io
from mido import MidiFile, MidiTrack, Message
from keras.models import load_model
import pretty_midi
from scipy.io import wavfile

def generate_music():

    # midi_file = "generated_melody.mid"
    # midi_data = pretty_midi.PrettyMIDI(midi_file)
    # audio_data = midi_data.fluidsynth()
    # audio_data = np.int16(
    #     audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    # )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.p
    # virtualfile = io.BytesIO()
    # wavfile.write(virtualfile, 44100, audio_data)
    # return virtualfile

    # Define the sequence length and the number of unique notes you want to generate
    sequence_length = 100
    unique_notes = 128  # Adjust based on your MIDI range (typically 128 for a full MIDI range)

    # Load the trained model
    loaded_model = load_model('generators/models/trained_model.h5')

    # Initialize the pattern with a random seed sequence of length sequence_length
    start = np.random.randint(0, unique_notes - 1)
    pattern = [start] * sequence_length
    generated_notes = []

    for i in range(500):  # Adjust the length of the generated melody
        x = np.reshape(pattern, (1, sequence_length, 1))
        x = x / float(unique_notes)
        prediction = loaded_model.predict(x, verbose=0)

        # Apply temperature for randomness control
        temperature = 0.7  # Experiment with different values
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
        msg = Message('note_on', note=note, velocity=64, time=100)
        output_track.append(msg)

        msg = Message('note_off', note=note, velocity=64, time=100)
        output_track.append(msg)

    # return output_midi_file
    # output_midi_file.save('generated_melody.mid')
    res=bytes(generated_notes)
    res2=np.frombuffer(res, dtype=np.uint8)

    rescaled_array2=np.sin(res2* 10 * 2 * np.pi)

    # Step 1: Normalize the values to [0, 1]
    min_value = np.min(rescaled_array2)
    max_value = np.max(rescaled_array2)
    normalized_array = (rescaled_array2 - min_value) / (max_value - min_value)

    # Step 2: Rescale the values to the desired range
    desired_min = -0.5  # Replace with your desired minimum value
    desired_max = 0.5  # Replace with your desired maximum value
    rescaled_array = (normalized_array * (desired_max - desired_min)) + desired_min

    print(type(rescaled_array))
    print(rescaled_array)
    return rescaled_array
