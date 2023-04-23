import pickle
import os
import pandas as pd

from os.path import dirname, abspath, join
BD = abspath(dirname(__file__))


def prepare_zipcode(df : pd.DataFrame) -> dict[int:float]:
    #create zipcode conversion table
    zipcode = {}

    #dropnan from prices
    df2 = df.dropna(subset=['Price'])
    #dropnan from zipcode
    df2 = df2.dropna(subset=['zipcode'])

    for z in list(df2['zipcode'].unique()):
        zipcode[z] = df2[df2['zipcode'] == z]['Price'].median()
        
    return zipcode

def prepare_type(df : pd.DataFrame) -> dict[str:float]:
    #create type conversion table
    types = {}

    #dropnan from prices
    df2 = df.dropna(subset=['Price'])
    #dropnan from type
    df2 = df2.dropna(subset=['type'])

    for i in df["type"].unique():
        types[i] = df[df['type'] == i]['Price'].mean()

    return types

def prepare_tax(df : pd.DataFrame) -> dict[int:float]:
    #create zipcode conversion table
    zipcode = {}

    #dropnan from tax
    df2 = df.dropna(subset=['Taxe'])
    #dropnan from zipcode
    df2 = df2.dropna(subset=['zipcode'])

    for z in list(df2['zipcode'].unique()):
        zipcode[z] = df2[df2['zipcode'] == z]['Taxe'].mean()

    return zipcode

def get_name(zipcode : int) -> str:

    if zipcode < 1300:
        return 'BruxellesCapitale'
    elif zipcode < 1500:
        return 'ProvinceduBrabantwallon'
    elif zipcode < 2000:
        return 'ProvinceduBrabantflamand'
    elif zipcode < 3000:
        return 'ProvincedAnvers'
    elif zipcode < 3500:
        return 'ProvinceduBrabantflamand2'
    elif zipcode < 4000:
        return 'ProvincedeLimbourg'
    elif zipcode < 5000:
        return 'ProvincedeLiege'
    elif zipcode < 6000:
        return 'ProvincedeNamur'
    elif zipcode < 6600:
        return 'ProvinceduHainaut1'
    elif zipcode < 7000:
        return 'ProvincedeLuxembourg'
    elif zipcode < 8000:
        return 'ProvinceduHainaut2'
    elif zipcode < 9000:
        return 'ProvincedeFlandreOccidentale'
    elif zipcode < 10000:
        return 'ProvincedeFlandreOrientale'
    else:
        return ""

def models_loader() -> dict[str : any]:
    #get the all the file name in the model folder 
    models = {} 
    for file in os.listdir(join(BD, 'models')):
        if file.endswith(".pickle"):
            name = file[:-7]

            models[name] = pickle.load(open(join(BD, 'models', file), 'rb'))

    return models

def check(immo : str, zipcode : str, room : str, surface : str) -> str:
    result = ""
    if immo == "":
        result += "<br> Please choose a category <br/>"

    if zipcode == "":
        result += "<br> Please enter a zipcode <br/>"
    else:
        zipcode = int(zipcode)
        if zipcode < 1000 or zipcode > 9999:
            result += "<br> Please enter a plausible zipcode <br/>"

    if room == "":
        result += "<br> Please enter a number of room <br/>"

    else:
        room = int(room)
        if room < 1 or room > 100:
             result += "<br> Please enter a plausible number of room <br/>"


    if surface == "":
        result += "<br> Please enter a living area <br/>"

    else:
        surface = float(surface)
        if surface < 5 or surface > 1000:
            result += "<br> Please enter a plausible living area <br/>"

    return result