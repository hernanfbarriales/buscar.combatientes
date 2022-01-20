######################################################################################################################################################################################
### Description: This program allows us to search any term in all the descriptors of the database. The program has a single input (busqueda), which can have multiple words, and   ###
### uses the MySQL database "busqueda", using the FULLTEXT search                                                                                                                  ###
######################################################################################################################################################################################
def btot(busqueda):

#Create connection with the MySQL database (the actual information has been replaced with ************ for security reasons)
    import MySQLdb
    import pandas as pd
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    db=MySQLdb.connect(
        host='************.mysql.pythonanywhere-services.com',
        user='************',
        passwd='************',
        db='************')

#Initiate the cursor that will read the MySQL database.    
    cursor = db.cursor ()
#To ensure there are no temp table, we try/except to drop it.
    try:
        cursor.execute ("DROP TABLE temp")
    except:
        pass
#Create a temp table with a limit of 25,000 results provided with the FULLTEXT search when compared to our search term.
    cursor.execute ("CREATE TABLE temp SELECT * FROM busqueda WHERE MATCH(loc) AGAINST ('{}') LIMIT 25000".format(busqueda.strip()))
#Out of that temp table, stored up to 10,000 results that contains exactly the same term (this step is necessary, as the FULLTEXT search includes approximated results, and we are
#interested in exact results).
    cursor.execute ("SELECT * FROM temp WHERE loc LIKE '%{}%' ORDER BY nombre ASC LIMIT 10000".format(busqueda.strip()))
    datos=cursor.fetchall()
#Drop temp table.
    cursor.execute("DROP TABLE temp")

#Create 4 empty lists to store all the different variables from the table busqueda.  
    link1=[]
    link2=[]
    nombre=[]
    info=[]

#Iterate the datos variable. it[0], it[1], it[2] are the name, surname1 and surname2, stored in temporal variables which will be used for the website's internal url
#(https://buscar.combatientes.es/resultados/name/surname1/surname2)...     
    for it in datos:
        if it[0]=='':
            temp1='-'
        else:
            temp1=it[0]
        if it[1]=='':
            temp2='-'
        else:
            temp2=it[1]
        if it[2]=='':
            temp3='-'
        else:
            temp3=it[2]
        link1.append('https://buscar.combatientes.es/resultados/{}/{}/{}'.format(temp1,temp2,temp3))
#Iterate the remaining items within the datos variable. it[3] is the external url (where the record leads to), it[4] the full name, and it[5] the descriptor.
        link2.append(it[3])
        nombre.append(it[4])
        info.append(it[5])

#To provide the total number of results, we use the length of one of the lists. If the length is 1, we write the phrase in singular ("There is 1 result"), if the length is 0, we
#indicate that there are no results, otherwise we write the sentence in plural ("There are 'length' results").
    if len(info)==1:
        total=('Se ha encontrado 1 registro para el término ')
    elif len(info)==0:
        total=('No se han encontrado registros para el término ')
    else:
        total=('Se han encontrado {} registros para el término '.format(len(info)))

#Close the connection to the database.
    cursor.close()
    db.close()

    return(nombre,info,link1,link2,total)
