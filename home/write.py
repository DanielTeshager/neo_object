"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.

"""
import csv
import json
from helpers import cd_to_datetime, datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`.
    Roughly, each output row corresponds to the information
    in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where
    the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w') as cf:
        writer = csv.DictWriter(cf, fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow({
                'datetime_utc': result.time,
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'designation': result._designation,
                'name': result.neo.name,
                'diameter_km': result.neo.diameter,
                'potentially_hazardous': result.neo.hazardous
            })


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly,
    the output is a list containing dictionaries, each mapping
    `CloseApproach`attributes to their values and the 'neo' key
    mapping to a dictionary of the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where
    the data should be saved.
    """
    data = []
    with open(filename, 'w') as jf:
        for result in results:
            data.append({
                'datetime_utc': datetime_to_str(result.time),
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'designation': result._designation,
                'neo': {
                    'designation': result.neo.designation,
                    'name': result.neo.name
                    if result.neo.name is not None else '',
                    'diameter_km': result.neo.diameter,
                    'potentially_haardous': result.neo.hazardous
                }
            })

        json.dump(data, jf)
