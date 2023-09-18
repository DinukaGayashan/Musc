import os


def get_model_names():
    directory = 'models/trained_models'
    files = [os.path.splitext(file)[0] for file in os.listdir(directory)]
    return files


def save_dataset(dataset_name,uploaded_files):
    folder_path=f'datasets/{dataset_name}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for uploaded_file in uploaded_files:
            with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getvalue())


# def save_model(name):
#     folder_path='models/trained_models'
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
    

