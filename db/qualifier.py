"""
@file: qualifier.py
@package: db
@description: Class to manage the qualifiers inside each column family.

@author: Samuel Chamalé
@date: may 2024
"""


class Qualifier:
    def __init__(self, max_versions=1):
        """
        Initialize the qualifier.

        Args:
            max_versions: The maximum number of versions to keep for the qualifier.
        """
        self.max_versions = max_versions
        self.data = {}
        self.current_version = 0

    def put(self, value):
        """
        Add a new value to the qualifier (Versioning is handled here).

        Args:
            value: The value to be added.
        """
        if len(self.data) == self.max_versions:
            # When reaching max versions, start overriding the oldest entries
            oldest_version = min(self.data.keys())
            del self.data[oldest_version]  # Remove the oldest version

        self.current_version += 1  # Increment the version number
        self.data[self.current_version] = value

    def get(self, version=None):
        """
        Retrieve the value of the qualifier.

        Args:
            version: The version of the qualifier to retrieve. If not provided, the most recent version is returned.
        """
        if version:
            return self.data.get(version, None)
        else:
            # If no version is specified, return the most recent version
            if self.data:
                return self.data[max(self.data.keys())]
            else:
                return None

    def scan(self):
        """
        Retrieve all versions of the qualifier.
        """
        return self.data

    def delete(self, version=None):
        """
        Delete a specific version of the qualifier or all versions.

        Args:
            version: The version of the qualifier to delete. If not provided, all versions are deleted.
        """
        if version:
            # Delete a specific version
            if version in self.data:
                del self.data[version]
        else:
            # Clear all versions
            self.data.clear()
