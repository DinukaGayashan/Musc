import os
import datetime


def get_model_names():
    directory = "models/trained_models"
    if not os.path.exists(directory):
        os.makedirs(directory)
    files = [os.path.splitext(file)[0] for file in os.listdir(directory)]
    return files


def get_melody_names():
    directory = "generated_melodies"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # files = [os.path.splitext(file)[0] for file in os.listdir(directory)]

    files_and_times = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        files_and_times[file] = creation_time

    del files_and_times['temp.midi']

    sorted_files_and_times = dict(sorted(files_and_times.items(), key=lambda item: item[1],reverse=True))
    return sorted_files_and_times


def is_model_available(model_name):
    return get_model_names().count(model_name) > 0


def save_dataset(dataset_name, uploaded_files):
    folder_path = f"datasets/{dataset_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for uploaded_file in uploaded_files:
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())


def save_model(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def save_melody(name, file):
    folder_path = "generated_melodies"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file.save(name)


def save_temp(name, file):
    folder_path = "generated_melodies"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file.dump(name)
