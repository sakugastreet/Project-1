#%%
import mysql.connector
from mysql.connector import Error

import pandas as pd

scriptures = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="notimportant",
                database="scriptures"
)
cursor = scriptures.cursor()

sql = f"""
SELECT 
    *
FROM 
    final_verse
"""
cursor.execute(sql)

# cursor.execute(sql)

    # Fetch all the rows
rows = cursor.fetchall()

    # Get column names from the cursor
columns = [col[0] for col in cursor.description]

    # Create a DataFrame from the fetched data
df = pd.DataFrame(rows, columns=columns)
df


#%%
for index, row in df.iterrows():
    sql = f"""
        INSERT INTO directory (dir, par_dir, verse_id)
        VALUES ("{"Verse " + str(row["verse_number"])}", {row["dir_id"]}, {row["id"]});
        """
    cursor.execute(sql)


#%%
for index, row in df.iterrows():
    print(row["book_title"])

#%%
# for title in df["volume_title"]:
sql = """
    SELECT
        *
    FROM
        directory
"""

cursor.execute(sql)
cursor.fetchall()


#%%
sql = """
    TRUNCATE TABLE directory
"""

cursor.execute(sql)
cursor.fetchall()




#%%
sql = f"""
        UPDATE directory
        SET
            par_dir = 101
        WHERE
            id = 1
        """
cursor.execute(sql)



#%%
scriptures.commit()