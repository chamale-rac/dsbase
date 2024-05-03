"""
@file: table.py
@package: db
@description: Central class that simulates HBase functionality, managing DDL and DML operations.

@author: Samuel Chamalé
@date: may 2024
"""


class Database:
    def __init__(self) -> None:
        """
        Initialize the database. Here should be load the initial state of the tables from file if needed.
        """
        self.tables = {}

    def create_table(self, table_name, column_families) -> str:
        """
        Create a new table in the data base

        Args:
            table_name (str): Name of the table
            column_families (list): List of column families

        Returns:
            str: Message with the result of the operation
        """

        if table_name in self.tables:
            return f"Table {table_name} already exists"

        self.tables[table_name] = column_families
        return f"Table {table_name} created"

    def list_tables(self) -> list:
        """
        List all tables in the data base

        Returns:
            list: List of tables
        """

        return list(self.tables.keys())

    def delete_table(self, table_name) -> str:
        """
        Delete a table from the data base

        Args:
            table_name (str): Name of the table

        Returns:
            str: Message with the result of the operation
        """

        if table_name not in self.tables:
            return f"Table {table_name} does not exist"

        del self.tables[table_name]
        return f"Table {table_name} deleted"


# Just for testing the basic Database object functionality
if __name__ == "__main__":
    db = Database()
    print(db.create_table("Usuarios", ["Info", "Contacto"]))
    print(db.list_tables())
    print(db.delete_table("Usuarios"))
    print(db.list_tables())
