import os
# import numpy as np
# from mido import MidiFile
# from keras.models import Sequential
# from keras.layers import LSTM, Dense, Flatten, TimeDistributed, Dropout, Embedding, Activation, GRU, Bidirectional
# import tensorflow as tf
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.utils import to_categorical
from glob import glob
from models.transformer import PopMusicTransformer
from ui import utility

def finetune_model(name):
    # declare model
    # utility.save_model(name)

    model = PopMusicTransformer(
        checkpoint="models/trained_models/REMI-tempo-checkpoint",
        is_training=True)
    # prepare data
    midi_paths = glob(f"datasets/{name}/*.mid*") # you need to revise it
    training_data = model.prepare_data(midi_paths=midi_paths)

    # check output checkpoint folder
    ####################################
    # if you use "REMI-tempo-chord-checkpoint" for the pre-trained checkpoint
    # please name your output folder as something with "chord"
    # for example: my-love-chord, cute-doggy-chord, ...
    # if use "REMI-tempo-checkpoint"
    # for example: my-love, cute-doggy, ...
    ####################################
    output_checkpoint_folder = f"models/trained_models/{name}" # your decision
    if not os.path.exists(output_checkpoint_folder):
        os.mkdir(output_checkpoint_folder)
    
    # finetune
    model.finetune(
        training_data=training_data,
        output_checkpoint_folder=output_checkpoint_folder)

    ####################################
    # after finetuning, please choose which checkpoint you want to try
    # and change the checkpoint names you choose into "model"
    # and copy the "dictionary.pkl" into the your output_checkpoint_folder
    # ***** the same as the content format in "REMI-tempo-checkpoint" *****
    # and then, you can use "main.py" to generate your own music!
    # (do not forget to revise the checkpoint path to your own in "main.py")
    ####################################

    # close
    model.close()



    # # Define the sequence length and the number of unique notes you want to generate
    # sequence_length = 100
    # # Adjust based on your MIDI range (typically 128 for a full MIDI range)
    # unique_notes = 128

    # # Directory containing your MIDI files
    # midi_directory = f"datasets/{name}"  # Replace with the path to your MIDI files directory

    # # Create lists to store input sequences and output sequences from multiple MIDI files
    # all_input_sequences = []
    # all_output_sequences = []

    # # Iterate through the MIDI files in the directory
    # for filename in os.listdir(midi_directory):
    #     if filename.endswith(".mid") or filename.endswith(".midi"):
    #         midi_file_path = os.path.join(midi_directory, filename)

    #         # Load and preprocess MIDI data
    #         midi = MidiFile(midi_file_path)

    #         notes = []

    #         for msg in midi.play():
    #             if msg.type == "note_on":
    #                 notes.append(msg.note)

    #         # Create input sequences and corresponding output sequences
    #         input_sequences = []
    #         output_sequences = []

    #         for i in range(0, len(notes) - sequence_length, 1):
    #             input_seq = notes[i:i + sequence_length]
    #             output_seq = notes[i + sequence_length]
    #             input_sequences.append(input_seq)
    #             output_sequences.append(output_seq)

    #         all_input_sequences.extend(input_sequences)
    #         all_output_sequences.extend(output_sequences)

    # # Prepare the data for training
    # X = np.reshape(all_input_sequences, (len(
    #     all_input_sequences), sequence_length, 1))
    # X = X / float(unique_notes)

    # y = np.array(all_output_sequences)
    # y = to_categorical(y, num_classes=unique_notes)

    # # Build the LSTM model
    # # model = Sequential()
    # # model.add(LSTM(256, input_shape=(
    # #     X.shape[1], X.shape[2]), return_sequences=True))
    # # model.add(LSTM(256))
    # # model.add(Dense(unique_notes, activation="softmax"))
    # # model.compile(loss="categorical_crossentropy", optimizer="adam")

    # model = Sequential()  
    # model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    # model.add(Dropout(0.2))  
    # model.add(LSTM(256))    
    # model.add(Flatten())  
    # model.add(Dense(256))  
    # model.add(Dropout(0.3))  
    # model.add(Dense(unique_notes, activation="softmax"))
    # model.compile(loss='categorical_crossentropy', optimizer='adam', run_eagerly=True)
    
    # # model = Sequential()
    # # model.add(Embedding(input_dim=50, output_dim=512, batch_input_shape=(16, 100)))  # Specify batch_input_shape
    # # model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True,stateful=True))
    # # model.add(Dropout(0.2))
    # # model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True,stateful=True))
    # # model.add(Dropout(0.2))
    # # model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True,stateful=True))
    # # model.add(Dropout(0.2))
    # # model.add(TimeDistributed(Dense(50)))
    # # model.add(Activation('softmax'))
    # # model.compile(loss='categorical_crossentropy', optimizer='adam')


    # # model = Sequential()

    # # # Add an Embedding layer to convert categorical data into continuous representations
    # # model.add(Embedding(input_dim=unique_notes, output_dim=100, input_length=X.shape[1]))

    # # # Add Bidirectional LSTM layers with more units
    # # model.add(Bidirectional(LSTM(512, return_sequences=True)))
    # # model.add(Dropout(0.3))

    # # # Add another Bidirectional LSTM layer
    # # model.add(Bidirectional(LSTM(512, return_sequences=True)))
    # # model.add(Dropout(0.3))

    # # # Use GRU layers for capturing different temporal dependencies
    # # model.add(GRU(256, return_sequences=True))
    # # model.add(Dropout(0.2))

    # # # Add a Dense layer with ReLU activation
    # # model.add(Dense(256, activation='relu'))
    # # model.add(Dropout(0.3))

    # # # Output layer with a softmax activation for multiclass classification
    # # model.add(Dense(256, activation="softmax"))

    # # # Compile the model with the Adam optimizer and categorical crossentropy loss
    # # model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))


    # # Fit the model with validation data and callbacks
    # model.fit(X, y, batch_size=128, epochs=50)
    

    # # Save the trained model to a file
    # utility.save_model(name,model)
