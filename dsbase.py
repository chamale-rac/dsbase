import cmd
import argparse
from ds.Database import Database


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

    #############################
    ###      DDL Commands     ###
    #############################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DSBase command line interface.")
    parser.add_argument("base_name", help="Name of the database.")
    args = parser.parse_args()

    DSBase(args.base_name).cmdloop()
