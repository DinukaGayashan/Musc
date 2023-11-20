import io

import numpy as np
import pretty_midi
from mido import MidiFile, MidiTrack, bpm2tempo, tempo2bpm
from scipy.io import wavfile

from ui import utility


def change_tempo_by_factor(midi_file, output_file, factor):
    midi = MidiFile(midi_file)
    new_midi = MidiFile()
    for track in midi.tracks:
        new_track = MidiTrack()
        for msg in track:
            if msg.type == 'set_tempo':
                original_tempo = tempo2bpm(msg.tempo)
                new_bpm = original_tempo * factor
                new_tempo = int(bpm2tempo(new_bpm))
                new_track.append(msg.copy(tempo=new_tempo))
            else:
                new_track.append(msg)
        new_midi.tracks.append(new_track)
    utility.save_melody(output_file, new_midi)


def limit_midi_duration(input_file, output_file, max_duration):
    midi_file = MidiFile(input_file)
    ticks_per_beat = midi_file.ticks_per_beat
    microseconds_per_beat = 500000
    for msg in midi_file:
        if msg.type == 'set_tempo':
            microseconds_per_beat = msg.tempo
    ticks_per_second = ticks_per_beat / microseconds_per_beat * 1000000
    last_tick = ticks_per_second * max_duration
    for track in midi_file.tracks:
        tick = 0
        keep = []
        for msg in track:
            if tick > last_tick:
                break
            keep.append(msg)
            tick += msg.time
        track.clear()
        track.extend(keep)
    utility.save_melody(output_file, midi_file)


def midi_to_wave(midi_file_name):
    midi_data = pretty_midi.PrettyMIDI(midi_file_name)
    audio_data = midi_data.fluidsynth()
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9)
    virtual_file = io.BytesIO()
    wavfile.write(virtual_file, 44100, audio_data)
    return virtual_file
