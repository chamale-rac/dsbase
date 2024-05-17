class Table:
    def __init__(self, table_name, column_families):
        self.table_name = table_name
        self.column_families = column_families
        self.is_enabled = True
