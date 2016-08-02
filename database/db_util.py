import sqlite3
from database import dbprops

def query_for_result(query, params):
    """Runs the query against the sqlite table and returns the result 
    as a list of dictionaries"""
    results = []
    with(sqlite3.connect(dbprops.sqlite_file)) as connection:
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute(query, params)
         
        for r in cur.fetchall():
            result = {}
            for field in r.keys():
                result[field]=r[field]
            results.append(result)
    return results
            
            
            
def insert(table, conn=None, data={}):
    """
     Generates and executes sql insert statement for field/value pairs 
     given as kwargs
    """
    fields = []
    values = []
    for key in data.keys():
        if key != None and key.strip()!="":
            fields.append(key.lower().replace(" ","_"))
            values.append(data[key])
    
    insert_stmt = "INSERT INTO "+str(table)+" "
    insert_stmt = insert_stmt+str(tuple(fields)).replace('"','')
    insert_stmt = insert_stmt+" VALUES ("
    #Loop n-1 '?,' characters first to avoid extra comma in statement 
    for v in range(1,len(values)):
        insert_stmt = insert_stmt+"?,"
    insert_stmt = insert_stmt+"?)"
    cursor = conn.cursor()
    cursor.execute(insert_stmt,tuple(values))
    conn.commit()
        
