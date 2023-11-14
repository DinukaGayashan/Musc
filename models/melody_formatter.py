from mido import MidiFile, MidiTrack, bpm2tempo, tempo2bpm
import numpy as np
import io
import pretty_midi
from scipy.io import wavfile
from ui import utility


def change_tempo_by_factor(midi_file, output_file, factor):
    # Load the MIDI file
    midi = MidiFile(midi_file)
    
    # Create a new MIDI file with the adjusted tempo
    new_midi = MidiFile()
    
    for track in midi.tracks:
        new_track = MidiTrack()
        for msg in track:
            if msg.type == 'set_tempo':
                # Calculate the new tempo based on the factor
                original_tempo = tempo2bpm(msg.tempo)
                new_bpm = original_tempo * factor
                new_tempo = int(bpm2tempo(new_bpm))
                new_track.append(msg.copy(tempo=new_tempo))
            else:
                new_track.append(msg)
        
        new_midi.tracks.append(new_track)
    
    # Save the new MIDI file
    utility.save_melody(output_file,new_midi)


def limit_midi_duration(input_file, output_file, max_duration):
    # Load the existing MIDI file
    midi_file = MidiFile(input_file)

    ticks_per_beat = midi_file.ticks_per_beat
    microseconds_per_beat = 500000  # Default tempo for MIDI files (120 BPM)

    for msg in midi_file:
        if msg.type == 'set_tempo':
            microseconds_per_beat = msg.tempo

    ticks_per_second = ticks_per_beat / microseconds_per_beat * 1000000

    lasttick = ticks_per_second*max_duration# last tick you want to keep
    # Rest of your code
    for track in midi_file.tracks:
        tick = 0
        keep = []
        for msg in track:
            if tick > lasttick:
                break
            keep.append(msg)
            tick += msg.time
        track.clear()
        track.extend(keep)

    # Save the modified MIDI file
    midi_file.save(output_file)


# def adjust_tempo_and_limit_duration(input_file,output_file, tempo_factor=1, max_duration_seconds=None):
#     midi_file = MidiFile(input_file)
#     new_midi = MidiFile()

#     for track in midi_file.tracks:
#         new_track = MidiTrack()
#         for msg in track:
#             if msg.type == 'set_tempo':
#                 # Calculate the new tempo based on the factor
#                 original_tempo = tempo2bpm(msg.tempo)
#                 new_bpm = original_tempo * tempo_factor
#                 new_tempo = int(bpm2tempo(new_bpm))
#                 new_track.append(msg.copy(tempo=new_tempo))
#             else:
#                 new_track.append(msg)
        
#         new_midi.tracks.append(new_track)

#         ticks_per_beat = new_midi.ticks_per_beat
#         microseconds_per_beat = 500000  # Default tempo for MIDI files (120 BPM)

#         for msg in new_midi:
#             if msg.type == 'set_tempo':
#                 microseconds_per_beat = msg.tempo

#         ticks_per_second = ticks_per_beat / microseconds_per_beat * 1000000

#         lasttick = ticks_per_second*max_duration_seconds*tempo_factor# last tick you want to keep
#         # Rest of your code
#         for track in new_midi.tracks:
#             tick = 0
#             keep = []
#             for msg in track:
#                 if tick > lasttick:
#                     break
#                 keep.append(msg)
#                 tick += msg.time
#             track.clear()
#             track.extend(keep)

#     utility.save_melody(output_file,new_midi)


def midi_to_wave(midi_file_name):
    midi_data = pretty_midi.PrettyMIDI(midi_file_name)
    audio_data = midi_data.fluidsynth()
    audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    )
    virtual_file = io.BytesIO()
    wavfile.write(virtual_file, 44100, audio_data)
    return virtual_file
