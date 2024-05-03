"""
@file: data_store.py
@package: data
@description: Manage the reading and writing of data in files (simulating the HFiles).

@author: Samuel Chamalé
@date: may 2024
"""

import json
import os


class DataStore:
    def __init__(self, data_directory="data"):
        """
        Initialize the DataStore with a specified directory for storing data files.

        Args:
          data_directory (str): The directory in which to store data files.
        """
        self.data_directory = data_directory
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

    def save_data(self, table_name, data) -> str:
        """
        Save data to a file corresponding to a table.

        Args:
          table_name (str): The name of the table for which data is being saved.
          data (dict): The data to be saved.

        Returns:
          str: success message.
        """

        file_path = os.path.join(self.data_directory, f"{table_name}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return f"Data for table {table_name} saved successfully ({file_path})"

    def load_data(self, table_name) -> dict:
        """
        Load data from a file corresponding to a table.

        Args:
            table_name (str): The name of the table for which data is being loaded.

        Returns:
            dict: The data loaded from the file.
        """

        file_path = os.path.join(self.data_directory, f"{table_name}.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        return {}


# Just for testing the basic DataStore object functionality
if __name__ == "__main__":
    ds = DataStore()
    sample_data = {
        '1': {'CF1:A': ('Val_1', 1591649830), 'CF1:B': ('Val_2', 1591649830)},
        '2': {'CF1:A': ('Val_3', 1591649830), 'CF1:B': ('Val_4', 1591649830)}
    }
    print(ds.save_data("Usuarios", sample_data))
    loaded_data = ds.load_data("Usuarios")
    print(loaded_data)
