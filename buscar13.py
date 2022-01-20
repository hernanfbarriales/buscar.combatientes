######################################################################################################################################################################################
### Description: This program provides all the results for a given full name (name, first surname, second surname), and groups them if more than one person relates to the same    ###
### record. The program has 3 inputs, name (nombre), first surname (apellido1) and second surname (apellido2), and uses the MySQL database "sumarios". Used for Type 1 Search.     ###
######################################################################################################################################################################################
def busqueda(nombre, apellido1, apellido2):

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
#Use the name, surname1 and surname2 inputted data to retrieve information about the document type (base), descriptor (loc), associated url (link), and identificator (id), sorted by 
#the position (pos) and the descriptor. The command strip has been added to remove any additional spaces included in the search terms.
    cursor.execute ("SELECT base,loc,link,id FROM sumarios WHERE nalt='{} {} {}' ORDER BY pos, loc ASC".format(nombre.strip(),apellido1.strip(),apellido2.strip()))

#Store all data in the variable "datos", and create empty lists for the document type (fondo), descriptor (info), urls (links) and id (diccionario).
    datos=cursor.fetchall()
    fondo=[]
    info=[]
    links=[]
    diccionario=[]

#Iterate the variable "datos" to populate each of the blank lists with all the relevant data for all the results of the searched full name.
    for it in datos:
        fondo.append(it[0])
        info.append(it[1])
        links.append(it[2])
#Here, we are also interested in providing any other name associated to the same id together with the searched name (for example, if someone was subjected to trial along with the
#person we are looking for). We extract all those names from the database, and order them alphabetically by the first surname.
        cursor.execute("SELECT ncomp FROM sumarios WHERE id='{}' ORDER BY ncomp ASC".format(it[3]))
        iteracion=pd.DataFrame(data=cursor.fetchall())
        diccionario.append(iteracion)

#To provide the total number of results, we use the length of one of the lists. If the length is 1, we write the phrase in singular ("There is 1 result"), if the length is 0, we
#indicate that there are no results, otherwise we write the sentence in plural ("There are 'length' results").
    if len(info)==1:
        total=('Se ha encontrado 1 registro a nombre de {} {} {}'.format(nombre.strip().title(),apellido1.strip().title(),apellido2.strip().title()))
    elif len(info)==0:
        total=('No se han encontrado registros a nombre de {} {} {}'.format(nombre.strip().title(),apellido1.strip().title(),apellido2.strip().title()))
    else:
        total=('Se han encontrado {} registros a nombre de {} {} {}'.format(len(info),nombre.strip().title(),apellido1.strip().title(),apellido2.strip().title()))

#Close the connection to the database.
    cursor.close()
    db.close()


    return(diccionario,links,fondo,info,total)
