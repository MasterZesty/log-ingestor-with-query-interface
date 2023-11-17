"""
A script demonstrating database interactions using MySQL and Python.

This script contains a Database class that facilitates interactions with a MySQL database,
including methods for retrieving logs based on filters and inserting log entries.

Dependencies:
    - mysql-connector-python
    - typing
    - logging

Usage:
    - Instantiate the Database class with database connection details.
    - Use the provided methods to interact with the database.

Author: Krishna Nimbalkar
Date: 17/11/2023

"""

import mysql.connector
from typing import Dict, List, Any
import logging

class Database:
    """
    A class to interact with a MySQL database.
    
    Attributes:
        user (str): The username for database access.
        password (str): The password for database access.
        host (str): The host address of the database.
        port (int): The port number of the database.
        database (str): The name of the database.
    """
    def __init__(self, user: str, password: str, host: str, port: int, database: str) -> None:
        """
        Initializes the Database class by establishing a connection to the MySQL database.

        Args:
            user (str): The username for database access.
            password (str): The password for database access.
            host (str): The host address of the database.
            port (int): The port number of the database.
            database (str): The name of the database.
        """
        try:
            self.connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            logging.error(f"Error connecting to the database: {e}")

    def create_tables(self):
        """Create tables in the database."""
        create_query = """
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            level VARCHAR(50),
            message VARCHAR(255),
            resourceId VARCHAR(50),
            timestamp DATETIME,
            traceId VARCHAR(50),
            spanId VARCHAR(50),
            commit VARCHAR(50),
            parentResourceId VARCHAR(50)
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_query)
        self.connection.commit()

    def get_logs_by_filter(self, filters: Dict[str, Any]) -> List[tuple[Any, ...]]:
        """
        Retrieves logs from the 'logs' table based on provided filter criteria.

        Args:
            filters (Dict[str, Any]): A dictionary containing filter criteria.

        Returns:
            List[Tuple[Any, ...]]: A list of tuples representing the retrieved logs.
        """
        try:
            query = "SELECT * FROM logs WHERE "
            conditions = []
            values = []

            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)

            query += " AND ".join(conditions)

            self.cursor.execute(query, tuple(values))
            filtered_logs = self.cursor.fetchall()
            return filtered_logs
        except mysql.connector.Error as e:
            logging.error(f"Error retrieving logs: {e}")
            return []

    def insert_log(self, log_data: Dict[str, Any]) -> None:
        """
        Inserts a log entry into the 'logs' table.

        Args:
            log_data (Dict[str, Any]): A dictionary containing log data to be inserted.
        """
        try:
            columns = ', '.join(log_data.keys())
            values_template = ', '.join(['%s'] * len(log_data))
            query = f"INSERT INTO logs ({columns}) VALUES ({values_template})"

            values = tuple(log_data.values())

            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as e:
            logging.error(f"Error inserting log: {e}")

    def close_connection(self) -> None:
        """
        Closes the database connection.
        """
        try:
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as e:
            logging.error(f"Error closing connection: {e}")


# Usage example:
if __name__ == "__main__":
    user = 'krishna'
    password = 'krishna'
    host = 'localhost'
    port = 3306
    database_name = 'log_ingestor_db'

    # example to insert records and search records
    try:
        db = Database(user, password, host, port, database_name)

        # create log table if it is not there
        db.create_tables()

        log_data = {
            'level': 'INFO',
            'message': 'This is an informational log message.',
            'resourceId': '12345',
            'timestamp': '2023-11-17 15:30:11',
            'traceId': 'ABCDE',
            'spanId': '123',
            'commit': 'abcd123',
            'parentResourceId': '5432022'
        }

        db.insert_log(log_data)

        filter_criteria = {
            'level': 'INFO',
            'message': 'This is an informational log message.',
            'resourceId': '12345',
            'timestamp': '2023-11-17 15:30:11',
            'traceId': 'ABCDE',
            'spanId': '123',
            'commit': 'abcd123',
            'parentResourceId': '5432022'
        }

        filtered_logs = db.get_logs_by_filter(filter_criteria)
        for log in filtered_logs:
            print(log)

    finally:
        db.close_connection()
