import os
import sqlite3
from croco_tools.exceptions import InvalidColumns
from croco_tools.types import Table
from typing import Any, Optional, Literal


class SqliteDatabase:
    def __init__(self, project_dir: str, database_name: str = 'database'):
        self.__database_path = os.path.join(project_dir, f'{database_name}.db')
        self.__cursor = None
        self.__connection = None
        self.__tables = None

    @property
    def database_path(self) -> str:
        return self.__database_path

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    @property
    def tables(self) -> list[Table] | None:
        return self.__tables

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> None:
        self.__connection = sqlite3.connect(self.database_path)
        self.__cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def create_table(self, table_name: str, columns: list[str] | list[Literal]) -> Table:
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        current_tables = self.tables

        table = Table(name=table_name, columns=columns)
        if current_tables:
            current_tables.append(table)
        else:
            current_tables = [table]

        self.__tables = current_tables

        self.cursor.execute(query)
        self.connection.commit()
        return table

    def select(self, table: Table, columns: Optional[list[str]] = '*', condition: Optional[str] = None):
        not_supported_columns = list(set(columns) - set(table.columns))
        if columns != '*' and not_supported_columns:
            raise InvalidColumns(columns, table)

        if columns:
            query = f"SELECT {', '.join(columns)} FROM {table.name}"
        else:
            query = f"SELECT * FROM {table.name}"

        if condition:
            query += f" WHERE {condition}"

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def insert(self, table: Table, values: list[Any], columns: Optional[list[str]] = None):
        columns = f'({", ".join(columns)})' if columns else None
        placeholders = '?, ' * (len(values) - 1) + '?'
        query = f"INSERT INTO {table.name} {columns} VALUES ({placeholders})"
        self.cursor.execute(query, values)

        self.connection.commit()
