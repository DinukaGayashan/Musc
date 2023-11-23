from glob import glob

from dotenv import dotenv_values

from models.transformer import PopMusicTransformer
from ui import utility

config = dotenv_values(".env")


def create_model(name, model=None, from_scratch=False):
    model = PopMusicTransformer(
        checkpoint=f"{config['TRAINED_MODELS_FOLDER']}/{model}",
        is_training=True, train_from_scratch=from_scratch)

    midi_paths = glob(f"{config['DATASET_FOLDER']}/{name}/*.mid*")
    training_data = model.prepare_data(midi_paths=midi_paths)

    output_checkpoint_folder = f"{config['TRAINED_MODELS_FOLDER']}/{name}"
    utility.save_model(output_checkpoint_folder)

    model.finetune(training_data=training_data,
                   output_checkpoint_folder=output_checkpoint_folder)
    model.close()
