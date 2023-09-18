import os
import numpy as np
from mido import MidiFile
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.utils import to_categorical
from ui import utility

def train_model(name):
    # Define the sequence length and the number of unique notes you want to generate
    sequence_length = 100
    # Adjust based on your MIDI range (typically 128 for a full MIDI range)
    unique_notes = 128

    # Directory containing your MIDI files
    midi_directory = f'datasets/{name}'  # Replace with the path to your MIDI files directory

    # Create lists to store input sequences and output sequences from multiple MIDI files
    all_input_sequences = []
    all_output_sequences = []

    # Iterate through the MIDI files in the directory
    for filename in os.listdir(midi_directory):
        if filename.endswith(".mid"):
            midi_file_path = os.path.join(midi_directory, filename)

            # Load and preprocess MIDI data
            midi = MidiFile(midi_file_path)

            notes = []

            for msg in midi.play():
                if msg.type == 'note_on':
                    notes.append(msg.note)

            # Create input sequences and corresponding output sequences
            input_sequences = []
            output_sequences = []

            for i in range(0, len(notes) - sequence_length, 1):
                input_seq = notes[i:i + sequence_length]
                output_seq = notes[i + sequence_length]
                input_sequences.append(input_seq)
                output_sequences.append(output_seq)

            all_input_sequences.extend(input_sequences)
            all_output_sequences.extend(output_sequences)

    # Prepare the data for training
    X = np.reshape(all_input_sequences, (len(
        all_input_sequences), sequence_length, 1))
    X = X / float(unique_notes)

    y = np.array(all_output_sequences)
    y = to_categorical(y, num_classes=unique_notes)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(
        X.shape[1], X.shape[2]), return_sequences=True))
    model.add(LSTM(256))
    model.add(Dense(unique_notes, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Train the model (you may need more epochs for better results)
    model.fit(X, y, epochs=10, batch_size=64)

    # Save the trained model to a file
    utility.save_model(name,model)
