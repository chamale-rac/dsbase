import cmd
from db.database import Database


class DatabaseCLI(cmd.Cmd):
    intro = 'Welcome to the simulated HBase system. Type help or ? to list commands.\n'
    prompt = '(hbase) '

    def __init__(self):
        super().__init__()
        self.db = Database()

    # DDL Commands
    def do_create_table(self, arg):
        "Create a table: create_table <table_name> <column_family_names separated by space>"
        args = arg.split()
        if len(args) < 2:
            print("Error: Specify table name and at least one column family name.")
            return
        table_name = args[0]
        column_families = args[1:]
        self.db.create_table(table_name, column_families)
        print(
            f"Table {table_name} created with column families {column_families}.")

    def do_list_tables(self, arg):
        "List all tables in the database."
        tables = self.db.list_tables()
        print("Tables:")
        for table in tables:
            print(table)

    def do_drop_table(self, arg):
        "Drop a table: drop_table <table_name>"
        self.db.drop_table(arg)
        print(f"Table {arg} dropped.")

    def do_describe_table(self, arg):
        "Describe the structure of a table: describe_table <table_name>"
        table = self.db.get_table(arg)
        if table:
            print(table.describe())
        else:
            print("Table not found.")

    # DML Commands
    def do_put(self, arg):
        "Insert or update a value: put <table_name> <row_key> <family_name> <qualifier_name> <value>"
        args = arg.split()
        if len(args) != 5:
            print(
                "Error: Specify table name, row key, family name, qualifier name, and value.")
            return
        table_name, row_key, family_name, qualifier_name, value = args
        table = self.db.get_table(table_name)
        if table:
            table.put(row_key, family_name, qualifier_name, value)
            print("Value inserted/updated successfully.")
        else:
            print("Table not found.")

    def do_get(self, arg):
        "Get a value: get <table_name> <row_key> <family_name> <qualifier_name>"
        args = arg.split()
        if len(args) != 4:
            print("Error: Specify table name, row key, family name, and qualifier name.")
            return
        table_name, row_key, family_name, qualifier_name = args
        table = self.db.get_table(table_name)
        if table:
            value = table.get(row_key, family_name, qualifier_name)
            print("Value:", value)
        else:
            print("Table not found.")

    def do_exit(self, arg):
        "Exit the application."
        print("Exiting...")
        return True


if __name__ == '__main__':
    DatabaseCLI().cmdloop()
