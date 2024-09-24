import sqlite3
from sqlite3 import Error



class DBInterface():
    def __init__(self):
        try:
            self.conn = sqlite3.connect("dataset.db")
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to database: {e}")

    def get_folder_contents(self, dir_id, table_name):
        """ Returns the ID's, Names, File_ID's and Tag_IDs of 
            each item with the given directory ID."""
        return self.select("ID, Name, File_ID", table_name, "Par_ID", f"{dir_id}")
    
    def set_state(self, dir_id, state_id):
        if self.is_folder(dir_id):
            for row in self.get_folder_contents(dir_id):
                self.set_state(row[0], state_id)
                
        else:
            self.update_table("Directory", "State_ID", state_id, "ID", dir_id)

    def get_file_contents(self, file_id):
        """ Returns the Name, Content, and Tag of the file found at ID."""
        # gets the file contents, 
        file = self.select("Name, Contents", "Files", "ID", f"{file_id}")

        
        return file[0][0], file[0][1]
    
    def add_folder(self, folder_name, par_id):
        self.insert("Directory", ["Name", "Par_ID"], [folder_name, par_id])
        return self.cursor.lastrowid

    def update_file(self, filename, contents, file_id):
        self.update_table("Files", "Name", filename, "ID", file_id)
        self.update_table("Files", "Contents", contents, "ID", file_id)
        self.update_table("Directory", "Name", filename, "File_ID", file_id)

    def add_file(self, par_id, filename, contents):
        # inserts into the "files" table, then grabs the id,
        # allowing for insertion in the directorys table
        self.insert("Files", ["Name", "Contents"], [filename, contents])
        file_id = self.cursor.lastrowid

        self.insert("Directory", ["Name", "Par_ID", "File_ID"], [filename, par_id, file_id])

        return file_id
    
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

            self.cursor.execute(sql, (where_y, ))
            rows = self.cursor.fetchall()

            return rows
        
        except Error as e:
            print(f"Error executing self.select: {e}")

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

            self.cursor.execute(sql, (where_y, ))
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
            print(f"Error Inserting to table {table}: {e}")

    def update_table(self, table_name:str, column:str, set_value, where_x, where_y):
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

    def get_par_id(self, dir_id):
        """Returns the par_ID of the one given"""
        if dir_id == 1 or dir_id == "1":
            return 1


        # print(self.select("Par_ID", "Directory", "ID", f"{dir_id}"))
        return self.select("Par_ID", "Directory", "ID", f"{dir_id}")[0][0]
    
    def is_folder(self, dir_id):

        
        result = self.select("File_ID", "Directory", "ID", f"{dir_id}")

        if not result:
            return True
        
        file_id = result[0][0]
    
        if file_id == None:
            return True
        else:
            return False
        
    
    def delete_from_DB(self, dir_id):
        try:
            # If File Deletes from "Files" table 
            if self.is_folder(dir_id) == False:
                self.delete("Files", "ID", f"{self.get_file_id(dir_id)}")

            contents = self.get_folder_contents(dir_id)

            if contents:
                for row in contents:
                    self.delete_from_DB(row[0])
                
            self.delete("Directory", "ID", f"{dir_id}")

        except Error as e:
            print(f"Error Deleting File: {e}")
    
    def delete(self, table:str, column:str, value:str):
        sql = f"""
        DELETE FROM {table}
        WHERE {column} = ?
        """
        
        self.cursor.execute(sql, (value, ))
        self.conn.commit()

    def get_file_id(self, dir_id):
        file_id = self.select("File_ID", "Directory", "ID", f"{dir_id}")[0][0]

        return file_id
        
    def move(self, dir_id, new_par_id):
        self.update_table("Directory", "Par_ID", f"{new_par_id}", "ID", dir_id)
        

    def copy(self, dir_id, loc_id):
        if self.is_folder(dir_id):
            # i need to get the info, then copy/insert it into the lines.
            # then i need to get the children of the file and recursively 
            # insert them
            filename = self.select("Name", "Directory", "ID", f"{dir_id}")
            if filename != None:
                filename = filename[0][0]
                new_dir = self.add_folder(filename, loc_id)
            else:
                print("There was an error getting the filename to copy, ending process")
                return
            
            contents = self.get_folder_contents(dir_id)
            if contents == None:
                return
                
            for row in contents:
                self.copy(row[0], new_dir)

        else:
            file = self.get_file_contents(self.get_file_id(dir_id))
            self.add_file(loc_id, file[0], file[1])
            

    def get_children(self, dir_id):
        self.get_folder_contents(dir_id)

        