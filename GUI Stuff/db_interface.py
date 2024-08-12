import mysql.connector
from mysql.connector import Error
import pandas as pd

class DBInterface():
    def __init__(self):
        try:
            self.scriptures = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="notimportant",
                database="scriptures"
            )
            self.cursor = self.scriptures.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")



    def execute(self, select, fro, where=""):
        try:
            sql = f"SELECT {select} FROM {fro} {where}"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            columns = [col[0] for col in self.cursor.description]

    # Create a DataFrame from the fetched data
            return pd.DataFrame(rows, columns=columns)

        except Error as e:
            print(f"Error executing query: {e}")
            return "empty"

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.scriptures:
                self.scriptures.close()
        except Error as e:
            print(f"Error closing the connection: {e}")

# Example usage:
# db = DBInterface()
# results = db.execute('column1, column2', 'table_name')
# db.close()
