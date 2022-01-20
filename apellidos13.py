######################################################################################################################################################################################
### Description: This program helps identify similar results to the ones we search, by varying one of the three search terms, permuting some terms, breaking the names down... The ###
### Jaro-Winkle method is also used for determining those records more likely to be the result of typos or transcription errors. The program has 3 inputs, name (nombre), first    ###
### surname (apellido1) and second surname (apellido2), and uses the MySQL database "apellidos10".                                                                                 ###
######################################################################################################################################################################################
def apellidos(nombre,apellido1, apellido2):

#Create connection with the MySQL database (the actual information has been replaced with ************ for security reasons)
    import MySQLdb
    import pandas as pd
    import numpy as np
    from Levenshtein import jaro
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    #Establecer conexion con la base de datos.
    db=MySQLdb.connect(
        host='************.mysql.pythonanywhere-services.com',
        user='************',
        passwd='************',
        db='************')

#Replace fields with "-" (coming from the URL) with blanks, as they may appear in the database.
    if nombre=='-':
        nombre=''
    if apellido1=='-':
        apellido1=''
    if apellido2=='-':
        apellido2=''

#Initiate the cursor that will read the MySQL database.
    cursor = db.cursor ()

###Equal surnames (apellido1, apellido2), different name (nombre)###
#Extract all names that have the same surname1 and surname2. This provides probable siblings of the person we are looking for, in addition to probable typos.
    cursor.execute ("SELECT nom FROM apellidos10 WHERE ap1='{}' AND ap2='{}'".format(apellido1.strip(),apellido2.strip()))
#Store all in a variable, and create an empty list (urls).
    resnombres=np.unique(cursor.fetchall())
    urls=[]
#Append all those names different from the existing name (nombre) in the "urls" list.
    for i in resnombres:
        if i!=nombre.strip():
            if i=='':
                i='-'
            urls.append(i)

###Equal name and first surname (nombre and apellido1), different second surname (apellido2)###
#Extract all surname2 that have the same name and surname1.
    cursor.execute ("SELECT ap2 FROM apellidos10 WHERE nom='{}' AND ap1='{}'".format(nombre.strip(),apellido1.strip()))
#Store all in a variable, and create an empty list (urls2)
    resap2=np.unique(cursor.fetchall())
    urls2=[]
#Append all those surname2 different from the existing surname2 (apellido2) in the "urls2" list.
    for i in resap2:
        if i!=apellido2.strip():
            if i=='':
                i='-'
            urls2.append(i)

###Equal name and second surname (nombre and apellido2), different first surname (apellido1)###
#Extract all surname1 that have the same name and surname2.
    cursor.execute ("SELECT ap1 FROM apellidos10 WHERE nom='{}' AND ap2='{}'".format(nombre.strip(),apellido2.strip()))
#Store all in a variable, and create an empty list (urls3)
    resap1=np.unique(cursor.fetchall())
    urls3=[]
#Append all those surname1 different from the existing surname1 (apellido1) in the "urls3" list.
    for i in resap1:
        if i!=apellido1.strip():
            if i=='':
                i='-'
            urls3.append(i)

###Permutation of surname1 (apellido1) and surname2 (apellido2), in case there was a trascription error and the surnames appear to be swapped###
    urls4=[]
#This is only applied if the surnames differ (there is no point in swapping the same surname)
    if apellido2!=apellido1:
        cursor.execute ("SELECT nom FROM apellidos10 WHERE nom='{}' AND ap1='{}' AND ap2='{}'".format(nombre.strip(),apellido2.strip(),apellido1.strip()))
#Append the result of swapping surnames to urls4.
        resapap=np.unique(cursor.fetchall())

        for i in resapap:
            if i=='':
                i='-'
            urls4.append(i)

#To ensure we don't show the same name, surname1 and surname2 as suggestions for other results, we use the following try/except commands to remove them out of urls, urls2 and urls3
    try:
        urls.remove(nombre.capitalize())
    except:
        pass
    try:
        urls3.remove(apellido1.upper())
    except:
        pass
    try:
        urls2.remove(apellido2.upper())
    except:
        pass

#Here, we use the Jaro-Winkler method (belonging to the Levenshtein library) to show on the left-hand side of the results page those records that are most likely to be typos or
#errors from the person indexing the result, or from the employee writing down the names of people. These will be stored in the empty lists lev1, lev2 and lev3.
    lev1=[]
    lev2=[]
    lev3=[]

#Similar results for names. We iterate through the urls list, and if the Jaro Winkler coefficient is above 0.85, it is stored in the lev1 list.
    i=0
    while i < len(urls):
        temp=jaro(nombre.title(),urls[i])
        if temp>0.85:
            lev1.append(urls[i].upper())
#Additionally, we add the inputted name or the "-" as a result that is worth to check if they exist in the urls list. 
        try:
            if urls[i]==nombre.title()[0] or urls[i]=='-':
                lev1.append(urls[i].upper())
        except:
            pass
        i=i+1

#Similar results for surname2. We iterate through the urls2 list, and if the Jaro Winkler coefficient is above 0.85, it is stored in the lev2 list.
    i=0
    while i < len(urls2):
        temp=jaro(apellido2.upper(),urls2[i])
        if temp>0.85:
            lev2.append(urls2[i].upper())
#Additionally, we add the inputted surname2 or the "-" as a result that is worth to check if they exist in the urls2 list. 
        try:
            if urls2[i]==apellido2.upper()[0] or urls2[i]=='-':
                lev2.append(urls2[i].upper())
        except:
            pass
        i=i+1
        
#Similar results for surname1. We iterate through the urls3 list, and if the Jaro Winkler coefficient is above 0.85, it is stored in the lev3 list.
    i=0
    while i < len(urls3):
        temp=jaro(apellido1.upper(),urls3[i])
        if temp>0.85:
            lev3.append(urls3[i].upper())
#Additionally, we add the inputted surname1 or the "-" as a result that is worth to check if they exist in the urls3 list. 
        try:
            if urls3[i]==apellido1.upper()[0] or urls3[i]=='-':
                lev3.append(urls3[i].upper())
        except:
            pass
        i=i+1

#Add all names that match the surnames, and whose name is contained in a compound name (for example, "Juan Antonio" if we were searching for "Juan").
    cursor.execute ("SELECT nom from apellidos10 where ap1='{}' and ap2='{}' and (nom like '% {}' or nom like '{} %')".format(apellido1,apellido2,nombre,nombre))
    resapap=np.unique(cursor.fetchall())
    for i in resapap:
        if i=='':
            i='-'
        lev1.append(i)

#If the name that is being searched is compound name (for example, "Juan Antonio"), break the name in two, and add if there is any result for the separate names (i.e.
#"Juan" and "Antonio").
    if ' ' in nombre.strip():
        temp=nombre.title().split()
        for i in temp:
            cursor.execute ("SELECT nom FROM apellidos10 WHERE nom='{}' AND ap1='{}' AND ap2='{}'".format(i,apellido1,apellido2))
            resapap=np.unique(cursor.fetchall())
            for m in resapap:
                if m=='':
                    m='-'
                lev1.append(m)

#Close the connection to the database.
    cursor.close()
    db.close()
    
#If the search terms are added to the lev1, lev2 and lev3, remove them. 
    try:
        lev1.remove(nombre.upper())
    except:
        pass
    try:
        lev2.remove(apellido1.upper())
    except:
        pass
    try:
        lev3.remove(apellido2.upper())
    except:
        pass
      
    return(urls, urls2, urls3,lev1,lev2,lev3,urls4)

