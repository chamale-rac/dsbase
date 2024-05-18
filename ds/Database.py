from .utils import checkDirectoryExists, loadJsonFile, createDirectory, createJsonFile, updateJsonFile, deleteJsonFile
from .constants import METADATA_TEMPLATE, METADATA_SAVE_NAME, BASES_PATH
from .Table import Table


class Database:
    def __init__(self, base_path):
        self.base_name = base_path
        self.base_path = BASES_PATH + base_path + '/'
        self.metadata = {}

        if checkDirectoryExists(self.base_path):
            self.metadata = self.loadMetadata()
        elif createDirectory(self.base_path):
            self.createMetadata()
            self.metadata = METADATA_TEMPLATE

    def table_exists(self, table_name):
        return table_name in self.metadata['tables']

    #############################
    ###      DDL Commands     ###
    #############################

    def create_table(self, table_name, column_families, max_versions=1, is_enabled=True):
        if self.table_exists(table_name):
            return False
        # First modify the metadata
        self.metadata['tables'][table_name] = {
            'column_families': column_families,
            'max_versions': max_versions,
            'is_enabled': is_enabled
        }

        # Then create the table in a json file
        table_path = self.base_path + table_name + '.json'
        if createJsonFile(table_path, {}):
            self.updateMetadata(self.metadata)
            return True
        return False

    def list_tables(self):
        return list(self.metadata['tables'].keys())

    def disable_table(self, table_name):
        if not self.table_exists(table_name):
            return False
        self.metadata['tables'][table_name]['is_enabled'] = False
        return self.updateMetadata(self.metadata)

    def enable_table(self, table_name):
        if not self.table_exists(table_name):
            return False
        self.metadata['tables'][table_name]['is_enabled'] = True
        return self.updateMetadata(self.metadata)

    def is_enabled(self, table_name):
        if not self.table_exists(table_name):
            return False
        return self.metadata['tables'][table_name]['is_enabled']

    def describe_table(self, table_name):
        if not self.table_exists(table_name):
            return False
        return self.metadata['tables'][table_name]

    def drop_table(self, table_name):
        if not self.table_exists(table_name):
            return False
        del self.metadata['tables'][table_name]

        # Now remove the table file
        table_path = self.base_path + table_name + '.json'
        deleteJsonFile(table_path)

        return self.updateMetadata(self.metadata)

    def drop_all_tables(self):
        for table in self.list_tables():
            self.drop_table(table)

    def alter_table(self, table_name, column_families, max_versions, is_enabled):
        # TODO: Cause this involves messing up with the content of the json file
        pass

    #############################
    ###   General Commands    ###
    #############################

    def get_status(self):
        return self.metadata['status']

    def get_version(self):
        return self.metadata['version']

    def get_whoami(self):
        return self.metadata['whoami']

    #############################
    ###   Database Metadata   ###
    #############################

    def loadMetadata(self):
        metadata = loadJsonFile(self.base_path + METADATA_SAVE_NAME)
        if metadata is None:
            self.createMetadata()
        return metadata

    def createMetadata(self, metadata=METADATA_TEMPLATE):
        if createJsonFile(self.base_path + METADATA_SAVE_NAME, metadata):
            return True
        return False

    def updateMetadata(self, metadata):
        self.metadata = metadata
        return updateJsonFile(self.base_path + METADATA_SAVE_NAME, metadata)

    #############################
    ###     DML Commands      ###
    #############################

    def put(self, table_name, row_id, col_family, col_name, value):
        if not self.table_exists(table_name):
            return False, "Table does not exist."
        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)
        return table.put(row_id=row_id, col_family=col_family, col_name=col_name, value=value)

    def get(self, table_name: str, row_id: str):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)

        return table.get(row_id)

    def scan(self, table_name):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)

        return table.scan()

    def delete(self, table_name, row_id, col_family, col_name, version):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)
        return table.delete(row_id, col_family, col_name, version)

    def delete_all(self, table_name, row_id: str):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)

        return table.delete_all(row_id)
