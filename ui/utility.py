import datetime
import os
import shutil

from dotenv import dotenv_values

config = dotenv_values(".env")


def get_dictionary():
    return f"{config['TRAINED_MODELS_FOLDER']}/{config['DICTIONARY_NAME']}"


def is_model_available(model_name):
    return model_name in get_model_names()


def get_model_names():
    directory = config['TRAINED_MODELS_FOLDER']
    if not os.path.exists(directory):
        os.makedirs(directory)
    files_and_times = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        creation_time = datetime.datetime.fromtimestamp(
            os.path.getctime(file_path))
        files_and_times[file] = creation_time
    del files_and_times[config['DICTIONARY_NAME']]
    sorted_files_and_times = dict(
        sorted(files_and_times.items(), key=lambda item: item[1], reverse=True))
    return sorted_files_and_times


def save_model(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def delete_model(name):
    folder_path = config['TRAINED_MODELS_FOLDER']
    file_path = os.path.join(folder_path, name)
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    folder_path = config['DATASET_FOLDER']
    file_path = os.path.join(folder_path, name)
    if os.path.exists(file_path):
        shutil.rmtree(file_path)


def save_dataset(dataset_name, uploaded_files):
    folder_path = f"{config['DATASET_FOLDER']}/{dataset_name}"
    delete_dataset(dataset_name)
    os.makedirs(folder_path)
    for uploaded_file in uploaded_files:
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())


def delete_dataset(dataset_name):
    folder_path = f"{config['DATASET_FOLDER']}/{dataset_name}"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def get_melody_name(name):
    return f"{config['MELODIES_FOLDER']}/{name}"


def get_melody_names():
    directory = config['MELODIES_FOLDER']
    if not os.path.exists(directory):
        os.makedirs(directory)
    files_and_times = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        creation_time = datetime.datetime.fromtimestamp(
            os.path.getctime(file_path))
        files_and_times[file] = creation_time
    del files_and_times[config['TEMP_MIDI_NAME']]
    sorted_files_and_times = dict(
        sorted(files_and_times.items(), key=lambda item: item[1], reverse=True))
    return sorted_files_and_times


def save_melody(name, file):
    folder_path = config['MELODIES_FOLDER']
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file.save(name)


def delete_melody(name):
    folder_path = config['MELODIES_FOLDER']
    file_path = os.path.join(folder_path, name)
    if os.path.exists(file_path):
        os.remove(file_path)


def save_temp(name, file):
    folder_path = config['MELODIES_FOLDER']
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file.dump(name)
