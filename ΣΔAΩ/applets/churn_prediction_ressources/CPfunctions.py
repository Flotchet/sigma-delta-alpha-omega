import pickle
import os

from os.path import dirname, abspath, join
BD = abspath(dirname(__file__))

def models_loader() -> dict[str : any]:
    #get the all the file name in the model folder 
    models = {} 
    for file in os.listdir(join(BD, 'models')):
        if file.endswith(".pickle"):
            name = file[:-7]

            models[name] = pickle.load(open(join(BD, 'models', file), 'rb'))

    return models
