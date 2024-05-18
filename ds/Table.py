from .utils import loadJsonFile, updateJsonFile
from .constants import BASES_PATH


class Table:
    def __init__(self, table_name, base_name, column_families, versions):
        self.table_name = table_name
        self.column_families = column_families
        self.is_enabled = True
        self.table_path = BASES_PATH + base_name + table_name + '.json'
        self.data = self.loadData(self.table_path)
        self.versions = versions

    def loadData(self, file_path):
        return loadJsonFile(file_path)

    def put(self, row_id, col_family, col_name, value):

        if not col_family in self.column_families:
            return False, "Column family not found in table"

        self.data[row_id] = {}
        self.data[row_id][col_family][col_name][value] = value

        return updateJsonFile(self.table_path, self.data)

    def scan(self):
        return self.data
