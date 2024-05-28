import cmd
import argparse
from ds.Database import Database
from ds.utils import printDict
import time


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper


class DSBase(cmd.Cmd):
    intro = "Welcome to DSBase. Type help or ? to list commands.\n"

    def __init__(self, base_path):
        super().__init__()
        self.database: Database = Database(base_path)
        self.prompt = f"(dsbase: {base_path}) "  # Use base_path in the prompt

    #############################
    ###   Core Commands       ###
    #############################

    def do_exit(self, arg):
        "Exit DSBase."
        return True

    def do_clear(self, arg):
        "Clear the screen."
        print("\033[H\033[J")

    #############################
    ###   General Commands    ###
    #############################

    @timing
    def do_status(self, arg):
        "Get the status of the database."
        print(self.database.get_status())

    @timing
    def do_version(self, arg):
        "Get the version of the database."
        print(self.database.get_version())

    @timing
    def do_whoami(self, arg):
        "Get the user of the database."
        print(self.database.get_whoami())

    #############################
    ###      DDL Commands     ###
    #############################

    @timing
    def do_create_table(self, arg):
        "Create a table: create_table <table_name> <max_versions> <is_enabled: true> <column_family_names separated by space>"
        args = arg.split()
        if len(args) < 4:
            print(
                "Error: Specify table name, max_versions, is_enabled, and at least one column family name.")
            return

        table_name = args[0]
        try:
            max_versions = int(args[1])
        except ValueError:
            print("Error: max_versions must be an integer.")
            return
        is_enabled = args[2].lower() == "true"
        column_families = args[3:]

        if self.database.create_table(table_name, column_families, max_versions, is_enabled):
            print(
                f"Table {table_name} created with column families {column_families}. Max versions: {max_versions}. Is enabled: {is_enabled}.")
        else:
            print(f"Table {table_name} already exists.")

    @timing
    def do_list(self, arg):
        "List all tables in the database."
        tables = self.database.list_tables()
        print("Tables:")
        for table in tables:
            print(table)

    @timing
    def do_disable(self, arg):
        "Disable a table: disable <table_name>"
        res = self.database.disable_table(arg)
        if res:
            print(f"Table {arg} disabled.")
        else:
            print(f"Table {arg} not found.")

    @timing
    def do_enable(self, arg):
        "Enable a table: enable <table_name>"
        res = self.database.enable_table(arg)
        if res:
            print(f"Table {arg} enabled.")
        else:
            print(f"Table {arg} not found.")

    @timing
    def do_is_enabled(self, arg):
        "Check if a table is enabled: is_enabled <table_name>"
        res = self.database.is_enabled(arg)
        if res:
            print(f"Table {arg} is enabled.")
        else:
            print(f"Table {arg} is disabled.")

    @timing
    def do_describe(self, arg):
        "Describe the structure of a table: describe <table_name>"
        res = self.database.describe_table(arg)
        if res:
            print("Table structure:")
            printDict(res)
        else:
            print(f"Table {arg} not found.")

    @timing
    def do_exists(self, arg):
        "Check if a table exists: exist <table_name>"
        res = self.database.table_exists(arg)
        if res:
            print(f"Table {arg} exists.")
        else:
            print(f"Table {arg} does not exist.")

    @timing
    def do_drop(self, arg):
        "Drop a table: drop <table_name>"
        res = self.database.drop_table(arg)
        if res:
            print(f"Table {arg} dropped.")
        else:
            print(f"Table {arg} not found.")

    @timing
    def do_drop_all(self, arg):
        "Drop all tables in the database."
        status, message = self.database.drop_all_tables()
        if status:
            print("All tables dropped.")
        else:
            print("Error dropping tables:", message)

    @timing
    def do_alter(self, arg):
        "Alter a table: alter <table_name> <flag> <value>\nFlags: DELETE, RENAME, ADD\nIMPORTANT: Use ':' for old_col: new_col for RENAME flag."
        args = arg.split()
        if len(args) < 3:
            print("Error: Specify table name, flag, and value.")
            return

        table_name, flag, value = args
        success, message = self.database.alter_table(table_name, flag, value)
        if success:
            print("Table altered successfully.")
        else:
            print("Error altering table:", message)

    #############################
    ###      DML Commands     ###
    #############################

    @timing
    def do_put(self, arg):
        "Put a value in a table: put <table_name> <row_id> <column_family> <column_qualifier> <value>"
        args = arg.split()
        if len(args) < 5:
            print(
                "Error: Specify table name, row id, column family, column qualifier, and value.")
            return

        table_name, row_id, col_family, col_name, value = args
        status, message = self.database.put(
            table_name, row_id, col_family, col_name, value)

        if status:
            print(
                f"Put value {value} in table {table_name}. Row id: {row_id}. Column family: {col_family}. Column qualifier: {col_name}.")
        else:
            print(f"Error: {message}")

    @timing
    def do_get(self, arg):
        "Get a value from a table: get <table_name> <row_id>"
        args = arg.split()
        if len(args) < 2:
            print("Error: Specify table name and row id.")
            return

        table_name, row_id = args
        status, data = self.database.get(table_name, row_id)

        if status:
            print("Data:")
            printDict(data)
        else:
            print(data)

    @timing
    def do_scan(self, arg):
        "Scan a table: scan <table_name>"
        status, data = self.database.scan(arg)

        if status:
            print("Data:")
            printDict(data)
        else:
            print(data)

    @timing
    def do_delete(self, arg):
        "Delete a value from a table: delete <table_name> <row_id> <column_family> <column_qualifier> <version>"
        args = arg.split()
        if len(args) != 5:
            print(
                "Error: Specify table name, row id, column family, column qualifier, and version.")
            return

        table_name, row_id, col_family, col_name, version = args
        status, message = self.database.delete(
            table_name, row_id, col_family, col_name, version)

        if status:
            print(
                f"Deleted value in table {table_name}. Row id: {row_id}. Column family: {col_family}. Column qualifier: {col_name}. Version: {version}.")
        else:
            print(f"Error: {message}")

    @timing
    def do_delete_all(self, arg):
        "Delete all values of a row from a table: delete_all <table_name> <row_id>"
        args = arg.split()
        if len(args) < 2:
            print("Error: Specify table name and row id.")
            return

        table_name, row_id = args
        status, message = self.database.delete_all(table_name, row_id)

        if status:
            print(f"Deleted all values of row {row_id} in table {table_name}.")
        else:
            print(f"Error: {message}")

    @timing
    def do_count(self, arg):
        "Count the number of rows in a table: count <table_name>"
        args = arg.split()
        if len(args) < 1:
            print("Error: Specify table name.")
            return

        table_name = args[0]
        status, count = self.database.count(table_name)

        if status:
            print(f"Number of rows in table {table_name}: {count}")
        else:
            print(count)

    @timing
    def do_truncate(self, arg):
        "Truncate a table: truncate <table_name>"
        status, message = self.database.truncate(arg)
        if status:
            print(f"Table {arg} truncated.")
        else:
            print(f"Error: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DSBase command line interface.")
    parser.add_argument("base_name", help="Name of the database.")
    args = parser.parse_args()

    DSBase(args.base_name).cmdloop()
