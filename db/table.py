"""
@file: table.py
@package: db
@description: Class to manage the tables inside the database.

@author: Samuel Chamalé
@date: may 2024
"""

from .row import Row


class Table:
    def __init__(self, column_family_names, max_versions=1):
        """
        Initialize the table.

        Args:
            column_family_names: A list containing the names of the column families.
            max_versions: The maximum number of versions to keep for each qualifier.
        """
        self.rows = {}
        self.column_family_names = column_family_names
        self.max_versions = max_versions
        self.is_enabled = True  # Tables are enabled by default

    # DDL Operations
    def create_row(self, row_key):
        """
        Create a new row in the table.

        Args:
            row_key: The key of the row.
        """
        if row_key not in self.rows:
            self.rows[row_key] = Row(
                row_key, self.column_family_names, self.max_versions)
        else:
            print("Row already exists.")

    def list_rows(self):
        """
        List all rows in the table.
        """
        return list(self.rows.keys())

    def disable(self):
        """
        Disable the table.
        """
        self.is_enabled = False

    def enable(self):
        """
        Enable the table.
        """
        self.is_enabled = True

    def is_table_enabled(self):
        """
        Check if the table is enabled.       
        """
        return self.is_enabled

    def drop_row(self, row_key):
        """
        Drop a row from the table.   

        Args:
            row_key: The key of the row to be dropped.     
        """
        if row_key in self.rows:
            del self.rows[row_key]

    def drop_all_rows(self):
        """
        Drop all rows from the table.
        """
        self.rows.clear()

    def describe(self):
        """
        Describe the table.
        """
        description = {}
        for row_key, row in self.rows.items():
            description[row_key] = {family: list(row.column_families[family].qualifiers.keys())
                                    for family in row.column_families}
        return description

    # DML Operations
    def put(self, row_key, family_name, qualifier_name, value):
        """
        Add a new value to the table.

        Args:
            row_key: The key of the row.
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier.
            value: The value to be added.        
        """
        if not self.is_enabled:
            print("Table is disabled.")
            return
        if row_key not in self.rows:
            self.create_row(row_key)
        self.rows[row_key].put(family_name, qualifier_name, value)

    def get(self, row_key, family_name, qualifier_name, version=None):
        """
        Retrieve the value of the qualifier.

        Args:
            row_key: The key of the row.
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier.
            version: The version of the qualifier to retrieve. If not provided, the most recent version is returned.        
        """
        if row_key in self.rows:
            return self.rows[row_key].get(family_name, qualifier_name, version)
        return None

    def scan(self, row_key=None):
        """
        Retrieve all qualifiers of the row.

        Args:
            row_key: The key of the row to scan. If not provided, all rows are scanned.
        """
        if row_key and row_key in self.rows:
            return {row_key: self.rows[row_key].scan()}
        elif row_key:
            return None  # Row does not exist
        else:
            return {key: row.scan() for key, row in self.rows.items()}

    def delete(self, row_key, family_name=None, qualifier_name=None, version=None):
        """
        Delete a specific qualifier or all qualifiers of a row.

        Args:
            row_key: The key of the row.
            family_name: The name of the column family.
            qualifier_name: The name of the qualifier to delete. If not provided, all qualifiers are deleted.
            version: The version of the qualifier to delete. If not provided, all versions are deleted.
        """
        if row_key in self.rows:
            self.rows[row_key].delete(family_name, qualifier_name, version)

    def delete_all(self):
        """
        Delete all qualifiers of the table.
        """
        for row in self.rows.values():
            row.delete_all()

    def count(self):
        """
        Count the number of qualifiers in the table.
        """
        return sum(row.count() for row in self.rows.values())

    def truncate(self):
        """
        Truncate the table.

        This operation is equivalent to dropping all rows from the table.
        """
        self.disable()
        self.drop_all_rows()
        self.enable()
