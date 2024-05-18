from .utils import loadJsonFile, updateJsonFile
from .constants import BASES_PATH


class Table:
    def __init__(self, table_name, base_name, column_families, versions):
        self.table_name = table_name
        self.column_families = column_families
        self.is_enabled = True
        self.table_path = BASES_PATH + base_name + "/" + table_name + '.json'
        self.data = self.loadData(self.table_path)
        self.versions = versions

    def loadData(self, file_path):
        return loadJsonFile(file_path)

    def put(self, row_id: str, col_family: str, col_name: str, value: str):
        row_id = str(row_id)
        col_family = str(col_family)
        col_name = str(col_name)
        value = str(value)

        if not col_family in self.column_families:
            return False, "Column family not found in table"

        if row_id not in self.data:
            self.data[row_id] = {}

        if col_family not in self.data[row_id]:
            self.data[row_id][col_family] = {}

        if col_name not in self.data[row_id][col_family]:
            self.data[row_id][col_family][col_name] = {}

        # Handling versions
        value_versions = self.data[row_id][col_family][col_name]
        if not value_versions:
            next_version = 1
        else:
            next_version = max([
                int(key) for key in value_versions.keys()
            ]) + 1

        value_versions[str(next_version)] = value

        # If the number of versions exceeds 'self.versions', remove the version with the smallest key
        if len(value_versions) > self.versions:
            min_version = min([
                int(key) for key in value_versions.keys()
            ])
            del value_versions[str(min_version)]

        self.data[row_id][col_family][col_name] = value_versions

        return updateJsonFile(self.table_path, self.data), "Data inserted successfully"

    def get(self, row_id: str):
        row_id = str(row_id)

        if row_id not in self.data:
            return False, "Row not found in table"

        return True, self.data[row_id]

    def scan(self):
        return True, self.data

    # ‘<table name>’, ‘<row>’, ‘<column name >’, ‘<time stamp>’
    def delete(self, row_id: str, col_family: str, col_name: str, version: str):
        row_id = str(row_id)
        col_family = str(col_family)
        col_name = str(col_name)

        try:
            version = int(version)
        except:
            return False, "Version should be an integer"

        if not col_family in self.column_families:
            return False, "Column family not found in table"

        if row_id not in self.data:
            return False, "Row not found in table"

        if col_family not in self.data[row_id]:
            return False, "Column family not found in row"

        if col_name not in self.data[row_id][col_family]:
            return False, "Column name not found in column family"

        value_versions = self.data[row_id][col_family][col_name]

        if str(version) not in value_versions.keys():
            return False, "This version does not exist"

        del value_versions[str(version)]  # Delete the specified version

        # If the number of versions exceeds 'self.versions', remove the version with the smallest key
        if len(value_versions) > self.versions:
            min_version = min([
                int(key) for key in value_versions.keys()
            ])
            del value_versions[str(min_version)]

        self.data[row_id][col_family][col_name] = value_versions

        return updateJsonFile(self.table_path, self.data), "Data deleted successfully"

    def delete_all(self, row_id: str):
        row_id = str(row_id)

        if row_id not in self.data:
            return False, "Row not found in table"

        print(self.data)
        del self.data[row_id]
        print(self.data)

        return updateJsonFile(self.table_path, self.data), "Data deleted successfully"

    def count(self):
        return True, len(self.data)
