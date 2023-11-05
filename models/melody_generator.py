import numpy as np
import io
import pretty_midi
import uuid
from scipy.io import wavfile
from ui import utility
from models.transformer import PopMusicTransformer

def generate_music(model, duration, tempo, temperature):

    model = PopMusicTransformer(
        checkpoint=f"models/trained_models/{model}",
        is_training=False)
    
    model.generate(
        n_target_bar=16,
        temperature=1.2)


    midi_file_name = f"generated_melodies/generated_melody_{uuid.uuid1()}.mid"


    # utility.save_melody(midi_file_name, output_midi_file)

    midi_data = pretty_midi.PrettyMIDI(midi_file_name)
    audio_data = midi_data.fluidsynth()
    audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    )
    virtual_file = io.BytesIO()
    wavfile.write(virtual_file, 44100, audio_data)
    return virtual_file
