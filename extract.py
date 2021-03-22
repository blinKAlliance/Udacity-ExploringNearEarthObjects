"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neoList = list()
    
    with open(neo_csv_path, newline='') as inFile:
        nearEarthObjs = csv.DictReader(inFile)
        for neoValue in nearEarthObjs:
            newNEO = NearEarthObject(name=dict(neoValue).get('name'), 
                                     designation=dict(neoValue).get('pdes'), 
                                     diameter=dict(neoValue).get('diameter'), 
                                     hazardous=dict(neoValue).get('pha'))
            neoList.append(newNEO)
            
    return neoList

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cadList = list()
    
    with open(cad_json_path) as inFile:
        closeApproachData = json.load(inFile)
        closeData = closeApproachData['data']
        values = {}
        
        for key in closeApproachData['fields']:
            values[key] = closeApproachData['fields'].index(key)
            
        for line in closeData:
            newCad = CloseApproach(designation=line[values['des']],
                                   time=line[values['cd']],
                                   distance=line[values['dist']],
                                   velocity=line[values['v_rel']])
            cadList.append(newCad)
        
    return cadList
