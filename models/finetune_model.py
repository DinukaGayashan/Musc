from glob import glob
from models.transformer import PopMusicTransformer
from ui import utility
from dotenv import dotenv_values

config=dotenv_values(".env")

def finetune_model(name):
    # declare model
    # utility.save_model(name)

    model = PopMusicTransformer(
        checkpoint=f"{config['TRAINED_MODELS_FOLDER']}/{config['DEFAULT_MODEL_NAME']}",
        is_training=True)
    # prepare data
    midi_paths = glob(f"{config['DATASET_FOLDER']}/{name}/*.mid*") # you need to revise it
    training_data = model.prepare_data(midi_paths=midi_paths)

    # check output checkpoint folder
    ####################################
    # if you use "REMI-tempo-chord-checkpoint" for the pre-trained checkpoint
    # please name your output folder as something with "chord"
    # for example: my-love-chord, cute-doggy-chord, ...
    # if use "REMI-tempo-checkpoint"
    # for example: my-love, cute-doggy, ...
    ####################################
    output_checkpoint_folder = f"{config['TRAINED_MODELS_FOLDER']}/{name}" # your decision
    utility.save_model(output_checkpoint_folder)
    
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
