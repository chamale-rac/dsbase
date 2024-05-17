from .utils import checkDirectoryExists, checkFileExists, loadJsonFile, createDirectory, createJsonFile
from .constants import METADATA_TEMPLATE, METADATA_SAVE_NAME, BASES_PATH
from .Table import Table


class Database:
    def __init__(self, base_path):
        self.base_path = BASES_PATH + base_path + '/'
        self.metadata = {}

        if checkDirectoryExists(self.base_path):
            self.metadata = self.loadMetadata()
        elif createDirectory(self.base_path):
            self.saveMetadata()
            self.metadata = METADATA_TEMPLATE

    def table_exists(self, table_name):
        return table_name in self.metadata['tables']

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
            self.saveMetadata()
            return True

    def list_tables(self):
        pass

    def drop_table(self, table_name):
        pass

    def get_table(self, table_name):
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
            self.saveMetadata()
        return metadata

    def saveMetadata(self, metadata=METADATA_TEMPLATE):
        if createJsonFile(self.base_path + METADATA_SAVE_NAME, metadata):
            return True
        return False
