"""
@file: family.py
@package: db
@description: Class to manage the column families inside each table.

@author: Samuel Chamalé
@date: may 2024
"""
from .qualifier import Qualifier


class Family:
    def __init__(self, max_versions=1):
        """
        Initialize the column family.

        Args:
            max_versions: The maximum number of versions to keep for each qualifier.
        """
        self.qualifiers = {}
        self.max_versions = max_versions

    def put(self, qualifier_name, value):
        """
        Add a new qualifier to the column family.

        Args:
            qualifier_name: The name of the qualifier to be added.
            value: The value to be added.
        """
        if qualifier_name not in self.qualifiers:
            self.qualifiers[qualifier_name] = Qualifier(
                max_versions=self.max_versions)
        self.qualifiers[qualifier_name].put(value)

    def get(self, qualifier_name, version=None):
        """
        Retrieve the value of the qualifier.

        Args:
            qualifier_name: The name of the qualifier to retrieve.
            version: The version of the qualifier to retrieve. If not provided, the most recent version is returned.
        """
        if qualifier_name in self.qualifiers:
            return self.qualifiers[qualifier_name].get(version)
        else:
            return None

    def scan(self, qualifier_name=None):
        """
        Retrieve all qualifiers in the column family.

        Args:
            qualifier_name: The name of the qualifier to retrieve. If not provided, all qualifiers are returned.
        """
        if qualifier_name:
            return {qualifier_name: self.qualifiers[qualifier_name].scan()} if qualifier_name in self.qualifiers else {}
        else:
            return {q_name: qual.scan() for q_name, qual in self.qualifiers.items()}

    def delete(self, qualifier_name, version=None):
        """
        Delete a specific qualifier or version of the qualifier.

        Args:
            qualifier_name: The name of the qualifier to delete.
            version: The version of the qualifier to delete. If not provided, all versions are deleted.
        """
        if qualifier_name in self.qualifiers:
            self.qualifiers[qualifier_name].delete(version)
            if not self.qualifiers[qualifier_name].data:
                del self.qualifiers[qualifier_name]
            return True
        return False

    def delete_all(self):
        """
        Delete all qualifiers in the column family.
        """
        self.qualifiers.clear()

    def count(self):
        """
        Count the number of qualifiers in the column family.
        """
        return sum(len(qual.data) for qual in self.qualifiers.values())
