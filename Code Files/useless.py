#%%
from DBI_Class import DBInterface

face = DBInterface()

#%%
sql = """
INSERT INTO State (State)
VALUES ("None")
"""

# face.conn.execute(sql)
# sql = """
# DELETE FROM Directory
# WHERE ID >= 2
# """

face.conn.execute(sql)

face.conn.commit()
#%%
sql = """
CREATE TABLE Directory_new(
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Par_ID INTEGER,
    File_ID INTEGER,
    State_ID INTEGER,
    FOREIGN KEY (Par_ID) REFERENCES Directory(ID),
    FOREIGN KEY (State_ID) REFERENCES State(ID),
    FOREIGN KEY (File_ID) REFERENCES Files(ID)
)
"""

face.conn.execute(sql)
#%%
sql = """
ALTER TABLE Directory_new
RENAME TO Directory
"""


face.conn.execute(sql)
#%%
face.get_par_id("2")


#%%
sql = """
DROP TABLE Directory_newx
"""


face.cursor.execute(sql)
# face.cursor.fetchall()[0][0]


#%%
dictionary = {"key1":1, "key2":2, "key3":3}

#%%
for item in dictionary.items():
    print(item)

#%%
face.set_state(3, 1)


face.conn.commit()