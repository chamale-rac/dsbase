import cmd
import argparse
from ds.Database import Database
from ds.utils import printDict


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

    # def do_help(self, arg): This is a built-in command

    #############################
    ###   General Commands    ###
    #############################

    def do_status(self, arg):
        "Get the status of the database."
        print(self.database.get_status())

    def do_version(self, arg):
        "Get the version of the database."
        print(self.database.get_version())

    def do_whoami(self, arg):
        "Get the user of the database."
        print(self.database.get_whoami())

    # TODO: consider adding a do_info for obtaining metadata.

    #############################
    ###      DDL Commands     ###
    #############################

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

    def do_list(self, arg):
        "List all tables in the database."
        tables = self.database.list_tables()
        print("Tables:")
        for table in tables:
            print(table)

    def do_disable(self, arg):
        "Disable a table: disable <table_name>"
        res = self.database.disable_table(arg)
        if res:
            print(f"Table {arg} disabled.")
        else:
            print(f"Table {arg} not found.")

    def do_enable(self, arg):
        "Enable a table: enable <table_name>"
        res = self.database.enable_table(arg)
        if res:
            print(f"Table {arg} enabled.")
        else:
            print(f"Table {arg} not found.")

    def do_is_enabled(self, arg):
        "Check if a table is enabled: is_enabled <table_name>"
        res = self.database.is_enabled(arg)
        if res:
            print(f"Table {arg} is enabled.")
        else:
            print(f"Table {arg} is disabled.")

    def do_describe(self, arg):
        "Describe the structure of a table: describe <table_name>"
        res = self.database.describe_table(arg)
        if res:
            print("Table structure:")
            printDict(res)
        else:
            print(f"Table {arg} not found.")

    def do_exists(self, arg):
        "Check if a table exists: exist <table_name>"
        res = self.database.table_exists(arg)
        if res:
            print(f"Table {arg} exists.")
        else:
            print(f"Table {arg} does not exist.")

    def do_drop(self, arg):
        "Drop a table: drop <table_name>"
        res = self.database.drop_table(arg)
        if res:
            print(f"Table {arg} dropped.")
        else:
            print(f"Table {arg} not found.")

    def do_drop_all(self, arg):
        "Drop all tables in the database."
        self.database.drop_all_tables()
        print("All tables dropped.")

    def do_alter(self, arg):
        raise NotImplementedError

    #############################
    ###      DML Commands     ###
    #############################

    def do_put(self, arg):
        "Put a value in a table: put <table_name> <row_key> <column_family> <column_qualifier> <value>"
        args = arg.split()
        if len(args) < 5:
            print(
                "Error: Specify table name, row key, column family, column qualifier, and value.")
            return

        table_name, row_key, column_family, column_qualifier, value = args
        status, message = self.database.put(
            table_name, row_key, column_family, column_qualifier, value)

        if status:
            print(f"Put value {value} in table {table_name}.")
        else:
            print(f"Error: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DSBase command line interface.")
    parser.add_argument("base_name", help="Name of the database.")
    args = parser.parse_args()

    DSBase(args.base_name).cmdloop()
