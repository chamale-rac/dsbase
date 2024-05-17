from .utils import checkDirectoryExists, checkFileExists, loadJsonFile, createDirectory, createJsonFile
from .constants import METADATA_TEMPLATE, METADATA_SAVE_NAME, BASES_PATH


class Database:
    def __init__(self, base_path):
        self.base_path = BASES_PATH + base_path + '/'
        self.metadata = {}

        if checkDirectoryExists(self.base_path):
            self.metadata = self.loadMetadata()
        elif createDirectory(self.base_path):
            self.saveMetadata()
            self.metadata = METADATA_TEMPLATE

    def create_table(self, table_name, column_families):
        pass

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
