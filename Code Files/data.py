#%%

import sqlite3
import pandas as pd

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dataset.db')
cursor = conn.cursor()


#%%
sql = """
INSERT INTO Directory (Name)
VALUES ("Files")

"""

cursor.execute(sql)


#%%
sql = """
CREATE TABLE Directory (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(20) NOT NULL,
    Par_ID INT,
    File_ID,
    Tag_ID,
    FOREIGN KEY (Par_ID) REFERENCES Directory(ID) ON DELETE CASCADE,
    FOREIGN KEY (File_ID) REFERENCES Files(ID),
    FOREIGN KEY (Tag_ID) REFERENCES Tags(ID) ON DELETE SET NULL
)
"""

cursor.execute(sql)

#%%
sql = """
CREATE TABLE Files (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(20) NOT NULL
)
"""

cursor.execute(sql)


#%%
sql = """
CREATE TABLE Tags (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(20) NOT NULL
)
"""

cursor.execute(sql)


#%%
conn.commit()

#%%
conn.close()