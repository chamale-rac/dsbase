from .utils import checkDirectoryExists, loadJsonFile, createDirectory, createJsonFile, updateJsonFile, deleteJsonFile, removeDirectory, renameFile
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
            return False, "Table already exists."

        # Check there are not repeated column families
        if len(column_families) != len(set(column_families)):
            return False, "Column families must be unique."

        # First modify the metadata
        self.metadata['tables'][table_name] = {
            'column_families': column_families,
            'max_versions': max_versions,
            'is_enabled': is_enabled
        }

        # Then create the table in a json file
        table_path_dir = self.base_path + table_name

        if not createDirectory(table_path_dir):
            return False, "Error creating table directory."

        column_families_path = table_path_dir + '/'

        for column_family in column_families:
            if not createJsonFile(column_families_path + column_family + '.json', {}):
                return False, "Error creating column family directory."

        return self.updateMetadata(self.metadata), "Table and column families created successfully."

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
        table_path = self.base_path + table_name

        if not removeDirectory(table_path):
            return False, "Error removing table directory."

        return self.updateMetadata(self.metadata)

    def drop_all_tables(self):
        for table_name in self.list_tables():
            self.drop_table(table_name)

    def alter_table(self, table_name, flag, value):
        if not self.table_exists(table_name):
            return False, "Table does not exist."

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        if flag in ["DELETE", "ADD", "RENAME"]:
            if flag == "DELETE":
                if not value in column_families:
                    return False, "Column family does not exist."

                status = deleteJsonFile(self.base_path + table_name +
                                        '/' + value + '.json')
                if not status:
                    return False, "Error deleting column family."

                del column_families[value]
            elif flag == "RENAME":
                old_col, new_col = value.split(':')
                if old_col not in column_families:
                    return False, "Column family does not exist."

                if new_col in column_families:
                    return False, "Column family already exists."

                if old_col == new_col:
                    return False, "No changes made. Column family names are the same."

                if renameFile(self.base_path + table_name + '/' + old_col + '.json', self.base_path + table_name + '/' + new_col + '.json'):
                    return False, "Error renaming column family."

                column_families[new_col] = column_families[old_col]
                del column_families[old_col]

            elif flag == "ADD":
                new_col = value
                if new_col in column_families:
                    return False, "Column family already exists."

                if not createJsonFile(self.base_path + table_name + '/' + new_col + '.json', {}):
                    return False, "Error creating column family."
        else:
            return False, "Invalid flag."

        return True, "Table altered successfully."
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

    def count(self, table_name):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        versions = self.metadata['tables'][table_name]['max_versions']
        column_families = self.metadata['tables'][table_name]['column_families']

        table = Table(table_name, self.base_name, column_families, versions)

        return table.count()

    def truncate(self, table_name):
        if not self.table_exists(table_name):
            return False, "Table does not exist"

        table_metadata = self.metadata['tables'][table_name]

        print("  - Disabling table...")
        if not self.disable_table(table_name):
            return False, "Error disabling table"

        print("  - Dropping table...")
        if not self.drop_table(table_name):
            return False, "Error dropping table"

        # Create the table again AKA recreate the table
        table_name = table_name
        column_families = table_metadata['column_families']
        versions = table_metadata['max_versions']
        is_enabled = True

        return self.create_table(table_name, column_families, versions, is_enabled)
