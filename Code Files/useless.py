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