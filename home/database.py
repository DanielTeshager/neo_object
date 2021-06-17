"""A database encapsulating collections of
near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes
        that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and
        close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches,
        and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # Create auxilary data structure the will make the lookup
        # by designation or name much faster
        self._neo_by_des = {}
        self._neo_by_name = {}

        # link approach and neo objects by using the designation
        # attribute as a primary key identifier
        for approach in self._approaches:
            neo = self.get_neo_by_designation(approach._designation)
            neo.approaches.append(approach)
            approach.neo = neo

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation
        of the NEO to search for.
        :return: The `NearEarthObject` with the desired
        primary designation, or `None`.
        """
        # Lookup neo object by it's name and add it neo_by_name
        # dictionary for efficiency
        if designation not in self._neo_by_des:
            for neo in self._neos:
                if neo.designation == designation:
                    self._neo_by_des[designation] = neo
                    return self._neo_by_des[designation]
            else:
                self._neo_by_des[designation] = None
                return self._neo_by_des[designation]
        else:
            return self._neo_by_des[designation]

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name.
        No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # Lookup neo object by it's designation and add it
        # neo_by_des dictionary for efficiency
        if name not in self._neo_by_name:
            for neo in self._neos:
                if neo.name == name:
                    self._neo_by_name[name] = neo
                    return self._neo_by_name[name]
            else:
                self._neo_by_name[name] = None
                return self._neo_by_name[name]
        else:
            return self._neo_by_name[name]

    def query(self, filters=()):
        """Query close approaches to generate those
        that match a collection of filters.

        This generates a stream of `CloseApproach` objects
        that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated
        in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters
        capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # Genearte a stream of approach objects that pass the filter criteria
        for approach in self._approaches:
            if all(filter(approach) for filter in filters):
                yield approach