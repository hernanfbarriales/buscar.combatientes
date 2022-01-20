######################################################################################################################################################################################
### Description: This program allows the search by a single term (name or surname). The program has a single input (termino), and uses the MySQL databases "busqueda", "similnom", ###
### "similap1" and "similap2". This is used for the Type 2 search (By name or surname).                                                                                            ###
######################################################################################################################################################################################
def bus10(termino):

#Create connection with the MySQL database (the actual information has been replaced with ************ for security reasons)
    import MySQLdb
    import pandas as pd
    import numpy as np
    #Eliminar numero maximo de filas y columnas que muestra pandas por defecto.
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    #Establecer conexion con la base de datos.
    db=MySQLdb.connect(
        host='************.mysql.pythonanywhere-services.com',
        user='************',
        passwd='************',
        db='************')

#We remove any extra spaces in the search term, and remove any apostrophe.
    temp=termino.strip()
    temp=temp.replace("'","")
#Initiate the cursor that will read the MySQL database.
    cursor = db.cursor ()
#Using the term we inputed (termino), we conduct 3 different searches.
#The first one, we assume the term is the name (nom), and extract all first (ap1) and second surnames (ap2) from the database.
#available in the database.
    cursor.execute ("SELECT ap1,ap2 FROM apellidos10 WHERE nom='{}'".format(temp))
    datos1=cursor.fetchall()
#The second one, we assume the term is the first surname (ap1), and extract all names (nom) and second surnames (ap2) from the database.
    cursor.execute ("SELECT nom,ap2 FROM apellidos10 WHERE ap1='{}'".format(temp))
    datos2=cursor.fetchall()
#The third one, we assume the term is the second surname (ap2), and extract all names (nom) and first surnames (ap1) from the database.
    cursor.execute ("SELECT nom,ap1 FROM apellidos10 WHERE ap2='{}'".format(temp))
    datos3=cursor.fetchall()
    ap1a=[]
    ap2a=[]
    links1=[]
    noma=[]
    ap2b=[]
    links2=[]
    nomb=[]
    ap1b=[]
    links3=[]

#Following, we create the internal links to the different full names created.
#Search item + Surname1 + Surname 2 (https://buscar.combatientes.es/resultados/termino/ap1/ap2)
    for it in datos1:
        temp1=it[0]
        temp2=it[1]
        if temp1=='':
            temp1='-'
        if temp2=='':
            temp2='-'
        ap1a.append(temp1)
        ap2a.append(temp2)
        links1.append('/resultados/{}/{}/{}'.format(temp,temp1,temp2))
#Name + Search item + Surname 2 (https://buscar.combatientes.es/resultados/nom/termino/ap2)
    for it in datos2:
        temp1=it[0]
        temp2=it[1]
        if temp1=='':
            temp1='-'
        if temp2=='':
            temp2='-'
        noma.append(temp1)
        ap2b.append(temp2)
        links2.append('/resultados/{}/{}/{}'.format(temp1,temp,temp2))
#Name + Surname 1 + Search item (https://buscar.combatientes.es/resultados/nom/ap1/termino)
    for it in datos3:
        temp1=it[0]
        temp2=it[1]
        if temp1=='':
            temp1='-'
        if temp2=='':
            temp2='-'
        nomb.append(temp1)
        ap1b.append(temp2)
        links3.append('/resultados/{}/{}/{}'.format(temp1,temp2,temp))

    temp1=''
    temp2=''
    temp3=''
    for i in range(len(temp)):
        s = list(temp)
        s[i] = '_'
        temp1=temp1+'nom LIKE \''+''.join(s)+'\' or '
        temp2=temp2+'ap1 LIKE \''+''.join(s)+'\' or '
        temp3=temp3+'ap2 LIKE \''+''.join(s)+'\' or '

    busnom=temp1[0:-4]
    busap1=temp2[0:-4]
    busap2=temp3[0:-4]
    cursor.execute ("SELECT nom FROM similnom WHERE {}".format(busnom))
    resnombres=np.unique(cursor.fetchall())
    urls=[]
    for i in resnombres:
        if i=='':
            i='-'
        urls.append(i)

    cursor.execute ("SELECT ap1 FROM similap1 WHERE {}".format(busap1))
    resap1=np.unique(cursor.fetchall())
    urls2=[]
    for i in resap1:
        if i=='':
            i='-'
        urls2.append(i)

    cursor.execute ("SELECT ap2 FROM similap2 WHERE {}".format(busap2))
    resap2=np.unique(cursor.fetchall())
    urls3=[]
    for i in resap2:
        if i=='':
            i='-'
        urls3.append(i)

    try:
        urls.remove(temp.capitalize())
    except:
        pass
    try:
        urls2.remove(temp.upper())
    except:
        pass
    try:
        urls3.remove(temp.upper())
    except:
        pass

    cursor.close()
    db.close()
    return(ap1a,ap2a,noma,ap2b,nomb,ap1b,links1,links2,links3,urls,urls2,urls3)
