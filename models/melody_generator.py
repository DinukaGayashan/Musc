import uuid

from dotenv import dotenv_values

from models import melody_formatter
from models.transformer import PopMusicTransformer

config = dotenv_values(".env")


def generate_music(model, duration, tempo, temperature):
    temp_name = f"{config['MELODIES_FOLDER']}/{config['TEMP_MIDI_NAME']}"
    midi_file_name = f"{config['MELODIES_FOLDER']}/generated_melody_{uuid.uuid1()}.midi"

    model = PopMusicTransformer(
        checkpoint=f"{config['TRAINED_MODELS_FOLDER']}/{model}")
    model.generate(
        name=temp_name,
        n_target_bar=duration * tempo,
        temperature=temperature)

    melody_formatter.change_tempo_by_factor(midi_file=temp_name, output_file=temp_name, factor=tempo)
    melody_formatter.limit_midi_duration(input_file=temp_name, output_file=midi_file_name, max_duration=duration)

    return melody_formatter.midi_to_wave(midi_file_name)
