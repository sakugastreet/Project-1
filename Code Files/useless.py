#%%
from DBI_Class import DBInterface

face = DBInterface()


#%%
stuff = face.insert("Tags", ["Name"], ["Scriptures"])
stuff

#%%
stuff = face.insert("Directory", ["Name","Par_ID", "File_ID"], ["Constellations", "1", "1"])
stuff


#%%

face.select("*", "Files", "Name", "'Constellations'")
#%%
face.get_folder_contents(1)

#%%
sql = """
ALTER TABLE Files
ADD COLUMN Contents TEXT;
"""


face.cursor.execute(sql)

#%%
face.add_file("1", "Names", "Billy, Bob, Joe")


#%%
face.select_joined("Directory.Name, Par_ID, Tags.Name as Tag", "Directory", "Tags", "Directory.Tag_id", "Tags.ID")

#%%
face.insert_tag("2", "1")
#%%
face.conn.commit()

#%%
face.get_file_contents(1, 1)