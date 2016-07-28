


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
        
        
        
        
if __name__=='__main__':
    insert(table="EMPLOYEES",name="Ryan",title="Developer2")