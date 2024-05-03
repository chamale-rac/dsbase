"""
@file: table.py
@package: db
@description: Class to manage specific operations of the tables.

@author: Samuel Chamalé
@date: may 2024
"""


class Table:
    def __init__(self,  table_name, column_families=None) -> None:
        """
        Initialize a new table

        Args:
            table_name (str): Name of the table
            column_families (list): An optional names of the column families to initialize the table
        """

        self.table_name = table_name
        self.column_families = {
            cf: {} for cf in column_families
        } if column_families else {}

    def add_column_family(self, cf_name) -> str:
        """
        Add a new column family to the table

        Args:
            cf_name (str): Name of the column family

          Returns:
            str: Message with the result of the operation
        """

        if cf_name in self.column_families:
            return f"Column family {cf_name} already exists"

        self.column_families[cf_name] = {}
        return f"Column family {cf_name} added"

    def delete_column_family(self, cf_name) -> str:
        """
        Delete a column family from the table

        Args:
            cf_name (str): Name of the column family

        Returns:
            str: Message with the result of the operation
        """

        if cf_name not in self.column_families:
            return f"Column family {cf_name} does not exist"

        del self.column_families[cf_name]
        return f"Column family {cf_name} deleted"

    def list_column_families(self) -> list:
        """
        List all column families in the table

        Returns:
            list: List of column families
        """

        return list(self.column_families.keys())


# Just for testing the basic Table object functionality
if __name__ == "__main__":
    table = Table("Usuarios", ["Info", "Contacto"])
    print(table.add_column_family("DatosAdicionales"))
    print(table.list_column_families())
    print(table.delete_column_family("Contacto"))
    print(table.list_column_families())
