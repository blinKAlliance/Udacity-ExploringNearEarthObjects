"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldNames = { 
       'datetime_utc': None, 'distance_au': None, 
       'velocity_km_s': None, 'designation': None, 
       'name': None, 'diameter_km': None, 'potentially_hazardous': None
    }
    
    with open(filename, 'w') as outFile:
        writer = csv.DictWriter(outFile, fieldNames)
        writer.writeheader()
        
        for result in results:
            cad = result.serialize()
            row = {
               'datetime_utc': cad['datetime_utc'],
               'distance_au': cad['distance_au'],
               'velocity_km_s': cad['velocity_km_s'],
               'designation': cad['neo']['designation'],
               'name': (cad['neo']['name'] 
                       if cad['neo']['name'] else 'None'),
               'diameter_km': cad['neo']['diameter_km'],
               'potentially_hazardous': ('True' if cad['neo']
                                        ['potentially_hazardous']
                                        else 'False'),
            }
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    output = list()
    for result in results:
        output.append(result.serialize())
        
    with open(filename, 'w') as outFile:
        json.dump(output, outFile)
