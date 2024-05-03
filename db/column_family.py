"""
@file: column_family.py
@package: db
@description: Class to manage the column families inside each table.

@author: Samuel Chamalé
@date: may 2024
"""


class ColumnFamily:
    def __init__(self, name):
        """
        Initialize a new column family with a given name.

        Args:
            name (str): The name of the column family.
        """
        self.name = name
        self.data = {}  # This will store the data more complexly

    def put(self, row_key, column, value, timestamp):
        """
        Insert or update a value in the column family under a specified row key and column.

        Args:
            row_key (str): The row key under which the value is stored.
            column (str): The column name within the column family.
            value (any): The value to be stored.
            timestamp (int): The timestamp of this value.

        Returns:
            str: Success message.
        """
        if row_key not in self.data:
            self.data[row_key] = {}
        self.data[row_key][column] = (value, timestamp)
        return f"Value set at {row_key}:{column} with timestamp {timestamp}"

    def get(self, row_key, column):
        """
        Retrieve a value from the column family by row key and column.

        Args:
            row_key (str): The row key for which the value is retrieved.
            column (str): The column from which to retrieve the value.

        Returns:
            tuple: The value and timestamp stored at the key, or None if the key or column does not exist.
        """
        if row_key in self.data and column in self.data[row_key]:
            return self.data[row_key][column]
        else:
            return None

    def delete(self, row_key, column):
        """
        Delete a value from the column family by row key and column.

        Args:
            row_key (str): The row key of the value to be deleted.
            column (str): The column from which to delete the value.

        Returns:
            str: Success or error message.
        """
        if row_key in self.data and column in self.data[row_key]:
            del self.data[row_key][column]
            return f"Value deleted from {row_key}:{column}"
        else:
            return f"No such entry ({row_key}:{column}) to delete"

    def scan(self):
        """
        Returns all data in the column family, formatted by row keys and columns.

        Returns:
            dict: All data organized by row keys and columns.
        """
        return self.data


# Just for testing the basic ColumnFamily object functionality
if __name__ == "__main__":
    cf = ColumnFamily("Info")

    print(cf.put("userID", "name", "Samuel", 1))
    print(cf.put("userID", "age", 24, 2))
    print(cf.put("userID", "city", "Guatemala", 3))

    print(cf.get("userID", "name"))
    print(cf.get("userID", "age"))
    print(cf.get("userID", "city"))

    print(cf.scan())

    print(cf.delete("userID", "age"))
    print(cf.scan())
