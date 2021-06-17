"""Extract data on near-Earth objects & close approaches from CSV & JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments
provided at the command line, and uses the resulting collections
to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing
    data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    csv_data = open(neo_csv_path)
    csv_reader = csv.DictReader(csv_data)

    return [NearEarthObject(**{
        'designation': row['pdes'],
        'name': row['name'],
        'hazardous': True if row['pha'] == 'Y' else False,
        'diameter': row['diameter']}) for row in csv_reader]
    csv_data.close()


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file
    containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    json_file = open(cad_json_path)
    json_data = json.load(json_file)
    return [CloseApproach(**{
            'designation': jd[0],
            'time': jd[3],
            'distance': float(jd[4]),
            'velocity': float(jd[7])})
            for jd in json_data['data'] if jd[0] is not None]
    json_file.close()
