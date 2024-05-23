from .utils import loadJsonFile, updateJsonFile
from .constants import BASES_PATH
import os


class Table:
    def __init__(self, table_name, base_name, column_families, versions):
        self.table_name = table_name
        self.base_name = base_name
        self.column_families = column_families
        self.is_enabled = True
        self.table_path = BASES_PATH + base_name + "/" + table_name + '/'
        self.versions = versions

    def loadFamily(self, col_family):
        print(self.table_path + col_family + '.json')
        return loadJsonFile(self.table_path + col_family + '.json')

    def saveFamily(self, col_family, family_data):
        return updateJsonFile(self.table_path + col_family + '.json', family_data)

    def put(self, row_id: str, col_family: str, col_name: str, value: str):
        row_id = str(row_id)
        col_family = str(col_family)
        col_name = str(col_name)
        value = str(value)

        if col_family not in self.column_families:
            return False, "Column family not found in table"

        family_data = self.loadFamily(col_family)
        if family_data is None:
            return False, "Error loading family data"

        if row_id not in family_data:
            family_data[row_id] = {}

        if col_name not in family_data[row_id]:
            family_data[row_id][col_name] = {}

        # Handling versions
        value_versions = family_data[row_id][col_name]
        if not value_versions:
            next_version = 1
        else:
            next_version = max([int(key) for key in value_versions.keys()]) + 1

        value_versions[str(next_version)] = value

        # If the number of versions exceeds 'self.versions', remove the version with the smallest key
        if len(value_versions) > self.versions:
            min_version = min([int(key) for key in value_versions.keys()])
            del value_versions[str(min_version)]

        family_data[row_id][col_name] = value_versions

        saved = self.saveFamily(col_family, family_data)

        if not saved:
            return False, "Error saving data"
        return True, "Data saved successfully"

    def get(self, row_id: str, col_family: str):
        row_id = str(row_id)
        col_family = str(col_family)

        if col_family not in self.column_families:
            return False, "Column family not found in table"

        family_data = self.loadFamily(col_family)

        if row_id not in family_data:
            return False, "Row not found in table"

        return True, self.data[col_family][row_id]

    def scan(self):
        all_data = {}
        for cf in self.column_families:
            family_data = self.loadFamily(cf)
            all_data[cf] = family_data
        return True, all_data

    # ‘<table name>’, ‘<row>’, ‘<column name >’, ‘<time stamp>’
    def delete(self, row_id: str, col_family: str, col_name: str, version: str):
        row_id = str(row_id)
        col_family = str(col_family)
        col_name = str(col_name)

        try:
            version = int(version)
        except ValueError:
            return False, "Version should be an integer"

        if col_family not in self.column_families:
            return False, "Column family not found in table"

        family_data = self.loadFamily(col_family)

        if row_id not in family_data:
            return False, "Row not found in table"

        if col_name not in family_data[row_id]:
            return False, "Column name not found in column family"

        value_versions = family_data[row_id][col_name]

        if str(version) not in value_versions.keys():
            return False, "This version does not exist"

        del value_versions[str(version)]  # Delete the specified version

        # If the number of versions exceeds 'self.versions', remove the version with the smallest key
        if len(value_versions) > self.versions:
            min_version = min([int(key) for key in value_versions.keys()])
            del value_versions[str(min_version)]

        self.data[col_family][row_id][col_name] = value_versions

        return self.saveFamily(col_family, family_data), "Data deleted successfully"

    def delete_all(self, row_id: str, col_family: str):
        row_id = str(row_id)
        col_family = str(col_family)

        if col_family not in self.column_families:
            return False, "Column family not found in table"

        family_data = self.loadFamily(col_family)

        if row_id not in family_data:
            return False, "Row not found in table"

        del family_data[row_id]

        return self.saveFamily(col_family, family_data), "Data deleted successfully"

    def count(self):
        rows = set()
        for cf in self.column_families:
            family_data = self.loadFamily(cf)
            if family_data is None:
                return False, "Error loading family data"
            family_data_keys = family_data.keys()
            rows.update(family_data_keys)
        return True, len(rows)
