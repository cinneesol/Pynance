


def insert(table, **kwargs):
    fields = []
    values = []
    for key in kwargs.keys():
        fields.append(key)
        values.append(kwargs[key])
    
    insert_stmt = "INSERT INTO "+str(table)+" "
    insert_stmt = insert_stmt+str(tuple(fields)).replace('"','')
    insert_stmt = insert_stmt+" VALUES ("
    #Loop n-1 '?,' characters first to avoid extra comma in statement 
    for v in range(1,len(values)):
        insert_stmt = insert_stmt+"?,"
    insert_stmt = insert_stmt+"?)"
    cursor = conn.cursor()
    cursor.execute(insert_stmt,str(tuple(values)))
    conn.commit()
        
        
        
        
if __name__=='__main__':
    insert(table="EMPLOYEES",name="Ryan",title="Developer2")