# Importamos la clase Table desde el archivo table.py
from table import Table


class Database:
    def __init__(self) -> None:
        """
        Initialize the database. Here should be load the initial state of the tables from file if needed.
        """
        self.tables = {}

    def create_table(self, table_name, column_families) -> str:
        """
        Create a new table in the database using the Table class to manage column families.

        Args:
            table_name (str): Name of the table
            column_families (list): List of column families

        Returns:
            str: Message with the result of the operation
        """
        if table_name in self.tables:
            return f"Table {table_name} already exists"

        # Aquí se crea un objeto de la clase Table con las familias de columnas proporcionadas
        self.tables[table_name] = Table(table_name, column_families)
        return f"Table {table_name} created successfully"

    def list_tables(self) -> list:
        """
        List all tables in the database

        Returns:
            list: List of table names
        """
        return list(self.tables.keys())

    def delete_table(self, table_name) -> str:
        """
        Delete a table from the database

        Args:
            table_name (str): Name of the table to be deleted

        Returns:
            str: Message with the result of the operation
        """
        if table_name not in self.tables:
            return f"Table {table_name} does not exist"

        del self.tables[table_name]
        return f"Table {table_name} deleted successfully"


# Just for testing the basic Database object functionality
if __name__ == "__main__":
    db = Database()
    print(db.create_table("Usuarios", ["Info", "Contacto"]))
    print(db.list_tables())
    print(db.delete_table("Usuarios"))
    print(db.list_tables())
