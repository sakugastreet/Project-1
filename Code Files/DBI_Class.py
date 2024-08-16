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
    
    def get_file_contents(self, id, tag_id):
        """ Returns the Name, Content, and Tag of the file found at ID."""
        # gets the file contents, 
        file = self.select("Name, Contents", "Files", "ID", f"{id}")
        # gets the tag and appends it to file
        if tag_id != "None":
            tag = self.select("Name", "Tags", "ID", f"{tag_id}")[0][0]
        else:
            tag = "None"

        total = [file[0][0], file[0][1], tag]
        return total
    
    def add_file(self, par_id, filename, contents, tag_id=""):
        # inserts into the "files" table, then grabs the id,
        # allowing for insertion in the directorys table
        self.insert("Files", ["Name", "Contents"], [filename, contents])
        file_id = self.cursor.lastrowid

        self.insert("Directory", ["Name", "Par_ID", "File_ID"], [filename, par_id, file_id])

        if tag_id != "":
            self.insert_tag(file_id, tag_id)

    def insert_tag(self, dir_id, tag_id):
        self.update_table("Directory", "Tag_ID", tag_id, "ID", dir_id)

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

    def select_joined(self, sel_entry, fro_entry, join, on_x, on_y, where_x="", where_y=""):
        try:    
            if where_x == "" or where_y == "":
                sql = f"""
                SELECT
                    {sel_entry}
                FROM
                    {fro_entry}
                JOIN
                    {join}
                ON
                    {on_x} = {on_y}
                """
            else:
                sql = f"""
                SELECT
                    {sel_entry}
                FROM
                    {fro_entry}
                JOIN
                    {join}
                ON
                    {on_x} = {on_y}
                WHERE
                    {where_x} = ?
                """

            self.cursor.execute(sql, where_y)
            rows = self.cursor.fetchall()

            return rows
        
        except Error as e:
            print(f"Error connecting to Files: {e}")

    def insert(self, table:str, columns:list, values:list):
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

    def update_table(self, table_name, column, set_value, where_x, where_y):
        try:
            sql = f"""
            UPDATE 
                {table_name}
            SET
                {column} = ?
            WHERE
                {where_x} = ?
            """

            self.cursor.execute(sql, (set_value, where_y))
            self.conn.commit()

        except Error as e:
            print(f"Error updating table: {e}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Error as e:
            print(f"Error closing the connection: {e}")


    