import uuid
from models import melody_formatter
from models.transformer import PopMusicTransformer
import time

def generate_music(model, duration, tempo, temperature):

    temp_name="generated_melodies/temp.midi"
    midi_file_name = f"generated_melodies/generated_melody_{uuid.uuid1()}.midi"

    start=time.time()

    model = PopMusicTransformer(
        checkpoint=f"models/trained_models/{model}")
    
    model.generate(
        name=temp_name,
        n_target_bar=duration*tempo,
        temperature=temperature)
    
    melody_formatter.change_tempo_by_factor(midi_file=temp_name,output_file=temp_name,factor=tempo)
    melody_formatter.limit_midi_duration(input_file=temp_name,output_file=midi_file_name,max_duration=duration)
    # melody_formatter.adjust_tempo_and_limit_duration(input_file=temp_name,output_file=midi_file_name,tempo_factor=tempo,max_duration_seconds=duration)

    end=time.time()
    print(f"Elapsed time: {end-start} seconds")
    
    return melody_formatter.midi_to_wave(midi_file_name)
