from .utils import loadJsonFile, updateJsonFile
from .constants import BASES_PATH


class Table:
    def __init__(self, table_name, base_name, column_families, versions):
        self.table_name = table_name
        self.column_families = column_families
        self.is_enabled = True
        self.table_path = BASES_PATH + base_name + "/" + table_name + '.json'
        print("table_path:", self.table_path, end="\n")
        self.data = self.loadData(self.table_path)
        self.versions = versions

    def loadData(self, file_path):
        return loadJsonFile(file_path)

    def put(self, row_id: str, col_family: str, col_name: str , value: str):

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

        self.data[row_id][col_family][col_name] = value

        return updateJsonFile(self.table_path, self.data), "Data inserted successfully"

    # ‘<table name>’, ‘<row>’, ‘<column name >’, ‘<time stamp>’
    def delete(self, row_id: str, col_family: str, col_name: str , version: str):

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

        del self.data[row_id][col_family][col_name]

        return updateJsonFile(self.table_path, self.data), "Data deleted successfully"
    
    def deleteall(self, row_id: str, col_family: str):

        row_id = str(row_id)
        col_family = str(col_family)

        if not col_family in self.column_families:
            return False, "Column family not found in table"

        if row_id not in self.data:
            return False, "Row not found in table"

        if col_family not in self.data[row_id]:
            return False, "Column family not found in row"

        del self.data[row_id][col_family]

        return updateJsonFile(self.table_path, self.data), "Data deleted successfully"

    def scan(self):
        return self.data
