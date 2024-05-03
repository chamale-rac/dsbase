"""
@file: column_family.py
@package: db
@description: Class to manage the column families inside each table.

@author: Samuel Chamalé
@date: may 2024
"""


class ColumnFamily:
    def __init__(self, cf_name):
        """
        Initialize a new column family with the given name.

        Args:
            cf_name (str): Name of the column family
        """

        self.cf_name = cf_name
        self.data = {}

    def put(self, key, value) -> str:
        """
        Insert or update a value in the column family under a specific key.

        Args:
            key (str): Key to identify the value
            value (str): Value to be stored

        Returns:
            str: Message with the result of the operation
        """

        self.data[key] = value
        return f"Value set at key {key} in {self.cf_name}"

    def get(self, key) -> any:
        """
        Retrieve a value from the column family by key.

        Args:
            key (str): The key for which the value is retrieved

        Returns:
            any: The value stored at the key, or None if the key does not exist
        """

        return self.data.get(key, None)

    def delete(self, key) -> str:
        """
        Delete a value from the column family by key.

        Args:
            key (str): The key for which the value is deleted

        Returns:c
            str: Message with the result of the operation
        """

        if key in self.data:
            del self.data[key]
            return f"Key {key} deleted from {self.cf_name}"

        return f"Key {key} not found in {self.cf_name}"

    def scan(self) -> dict:
        """
        Returns all key-value pairs in the column family.

        Returns:
            dict: Dictionary with all key-value pairs
        """
        return self.data


# Just for testing the basic ColumnFamily object functionality
if __name__ == "__main__":
    cf = ColumnFamily("Info")
    print(cf.put("userID", 101))
    print(cf.get("userID"))
    print(cf.scan())
    print(cf.delete("userID"))
    print(cf.scan())
