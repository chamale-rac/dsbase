"""
@file: row.py
@package: db
@description: Class to manage the rows inside each table.

@author: Samuel Chamalé
@date: may 2024
"""

from .family import Family


class Row:
    def __init__(self, row_key, families, max_versions=1, ):
        """
        Initialize the row.

        Args:
            row_key: The key of the row.
            max_versions: The maximum number of versions to keep for each qualifier.
            column_families: A dictionary containing the column families and their qualifiers.
        """
        self.row_key = row_key
        self.column_families = {name: Family(
            max_versions=max_versions) for name in families}
        self.max_versions = max_versions

    def put(self, family_name, qualifier_name, value):
        """
        Add a new value to the row.

        Args:
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier.
            value: The value to be added.
        """
        if family_name in self.column_families:
            self.column_families[family_name].put(qualifier_name, value)
        else:
            return None  # Return None if family name is not predefined

    def get(self, family_name, qualifier_name, version=None):
        """
        Retrieve the value of the qualifier.

        Args:
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier.
            version: The version of the qualifier to retrieve. If not provided, the most recent version is returned.
        """
        if family_name in self.column_families:
            return self.column_families[family_name].get(qualifier_name, version)
        return None

    def scan(self, family_name=None):
        """
        Retrieve all qualifiers of the row.

        Args:
            family_name: The name of the column family to scan. If not provided, all qualifiers are returned.        
        """
        if family_name and family_name in self.column_families:
            return {family_name: self.column_families[family_name].scan()}
        else:
            return {f_name: fam.scan() for f_name, fam in self.column_families.items()}

    def delete(self, family_name, qualifier_name=None, version=None):
        """
        Delete a specific qualifier or all qualifiers of a family.

        Args:
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier to delete. If not provided, all qualifiers are deleted.
            version: The version of the qualifier to delete. If not provided, all versions are deleted.
        """
        if family_name in self.column_families:
            if qualifier_name:
                self.column_families[family_name].delete(
                    qualifier_name, version)
            if not self.column_families[family_name].qualifiers:
                del self.column_families[family_name]  # Remove family if empty

    def delete_all(self):
        """
        Delete all qualifiers of the row.
        """

        self.column_families.clear()

    def count(self):
        return sum(fam.count() for fam in self.column_families.values())

    """
    Serialization methods
    """

    def to_dict(self):
        return {family_name: family.to_dict() for family_name, family in self.column_families.items()}

    @staticmethod
    def from_dict(data, row_key, max_versions):
        row = Row(row_key, [], max_versions)
        row.column_families = {name: Family.from_dict(
            family, max_versions) for name, family in data.items()}
        return row
