import sqlite3
from sqlite3 import Error



class DBInterface():
    def __init__(self):
        try:
            self.conn = sqlite3.connect("dataset.db")
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to database: {e}")

    def get_folder_contents(self, id):
        """ Returns the ID's, Names, File_ID's and Tag_IDs of 
            each item with the given directory ID."""
        return self.select("ID, Name, File_ID, Tag_ID", "Directory", "Par_ID", f"{id}")
    

    def get_file_contents(self, id):
        """ Returns the Name, Contents and Tags of the file found at ID."""
        return self.select("Name, ", "Files", "ID", f"{id}")


    def select(self, sel_entry, fro_entry, where_x="", where_y=""):
        try:    
            if where_x == "" or where_y == "":
                sql = f"""
                SELECT
                    {sel_entry}
                FROM
                    {fro_entry}
                """
            else:
                sql = f"""
                SELECT
                    {sel_entry}
                FROM
                    {fro_entry}
                WHERE
                    {where_x} = ?
                """

            self.cursor.execute(sql, where_y)
            rows = self.cursor.fetchall()

            return rows
        
        except Error as e:
            print(f"Error connecting to Files: {e}")

    def insert(self, table, columns, values):
        try:
            placeholders = ', '.join(['?'] * len(values))
            columns_formatted = ', '.join(columns)
            
            sql = f"""
                INSERT INTO 
                    {table} ({columns_formatted})
                VALUES
                    ({placeholders});
            """
            self.cursor.execute(sql, values)
            self.conn.commit()

        except Error as e:
            print(f"Error Inserting to Files: {e}")

    def update_table(self):
        pass

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Error as e:
            print(f"Error closing the connection: {e}")


    