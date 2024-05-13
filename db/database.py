"""
@file: database.py
@package: db
@description: Class to manage the database and its tables.

@author: Samuel Chamalé
@date: may 2024
"""

import os
import json

from .table import Table


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, column_family_names, max_versions=1):
        if table_name not in self.tables:
            self.tables[table_name] = Table(column_family_names, max_versions)
            return self.tables[table_name]
        else:
            return None  # Return None if table already exists

    def list_tables(self):
        return list(self.tables.keys())

    def drop_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]
            return True
        else:
            return None  # Return None if table does not exist

    def get_table(self, table_name):
        return self.tables.get(table_name, None)

    def describe_database(self):
        description = {table_name: table.describe()
                       for table_name, table in self.tables.items()}
        return description

    def truncate_database(self):
        for table in self.tables.values():
            table.truncate()
        return True

    def save_to_disk(self, directory):
        os.makedirs(directory, exist_ok=True)
        for table_name, table in self.tables.items():
            with open(os.path.join(directory, f"{table_name}.json"), 'w') as file:
                json.dump(table.to_dict(), file, indent=4)

    def load_from_disk(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.json'):
                table_name = file_name[:-5]  # remove '.json'
                with open(os.path.join(directory, file_name), 'r') as file:
                    data = json.load(file)
                # Placeholder for column_family_names and max_versions
                self.tables[table_name] = Table.from_dict(data, [], 1)
