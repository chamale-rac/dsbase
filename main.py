"""
@name: main.py
@description: Start point of the simulator, manage the ui and the execution flow.

@author: Samuel Chamalé
@date: may 2024
"""

import sys

from db.database import Database


def main():

    print("""
    THIS IS DSBASE!
    @version 0.1
    -- A simple database simulator inspired by Apache HBase
          
    (Type 'help' for a list of available commands or 'exit' to quit)        
    """)

    db = Database()

    while True:
        command = input(
            "> ").strip().lower()
        if command == "exit":
            print("Exiting the program.")
            break
        elif command == "help":
            print("Available commands:")
            print("create <table_name> <column_family1,column_family2,...> - Create a new table with specified column families")
            print("list - List all tables")
            print("drop <table_name> - Delete a specific table")
            print("drop all - Delete all tables")
            print("describe <table_name> - Show details of a specific table")
            # TODO: add more help descriptions as needed
        elif command.startswith("create "):
            parts = command.split()
            table_name = parts[1]  # get the table name
            column_families = parts[2].split(",") if len(
                parts) > 2 else []  # get the column families
            print(db.create_table(table_name, column_families))
        elif command == "list":
            print("Tables: ", db.list_tables())
        elif command.startswith("drop "):
            if command == "drop all":
                # Implement the logic to drop all tables
                pass
            else:
                table_name = command.split()[1]
                print(db.delete_table(table_name))
        elif command.startswith("describe "):
            table_name = command.split()[1]
            # Implement the logic to describe a table
            pass
        else:
            print("Invalid command, type 'help' for options.")


if __name__ == "__main__":
    main()
