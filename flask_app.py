###################################################################################################################################################################################
### We start importing those python libraries that will be required (from Flask: Flask, request, render_template and redirect), as well as the programs built for this search   ###
### engine (buscar13, apellidos13, bus10, btot).                                                                                                                                ###
###################################################################################################################################################################################
from flask import Flask, request,render_template, redirect
from buscar13 import busqueda
from apellidos13 import apellidos
from bus10 import bus10
from btot import btot

app = Flask(__name__)
app.config["DEBUG"] = True


###################################################################################################################################################################################
### Main page: It allows us to conduct 3 different types of searches: Type 1. Full name Search (name, surname1 and surname2), Type 2. Single name Search(name or surname).      ###
### Type 3. General Search (FULLTEXT search using the descriptor of all the records in the SQL table).                                                                          ###
###################################################################################################################################################################################
@app.route("/", methods=["GET", "POST"])
def mainpage():
    if request.method=="GET":
        return render_template("main_page.html")

#Remove ' (apostrophe) from entered fields "name", "surname1" and "surname2", as it doesn't work well with the SQL database.
    nombre=request.form["nombre"].replace("'","")
    apellido1=request.form["apellido1"].replace("'","")
    apellido2=request.form["apellido2"].replace("'","")

#To allow the results to be shared externally, a specific results' URL will be generated (https://buscar.combatientes.es/resultados/"Name"/"Surname1"/"Surname2"). For this
#to work even when some fields are left blank, we need to replace such blank spaces with the character "-"
    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    
#It was observed that many users simply inputted one of the 3 fields, leading to practically no results. In those cases, the Type 2 search (termino) may be better suited,
#so the results displayed will be those of that search type (https://buscar.combatientes.es/termino/"Name or Surname") 
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

###################################################################################################################################################################################
### Type 1 Search: When a Type 1 search is used, the user is redirected to the URL https://buscar.combatientes.es/resultados/Nombre/Apellido1/Apellido2. This helps in sharing  ###
### the results externally, saving them for later, or even carry out a direct search by modifying the URL.                                                                      ###
###################################################################################################################################################################################
@app.route('/resultados/<nombre>/<apellido1>/<apellido2>', methods=["GET", "POST"])
def resultados(nombre,apellido1,apellido2):
    if request.method=="GET":
#A new conversion is required, as we had previously changed any empty field for "-". In this step, if there is any field populated with "-", we remove it for searching in SQL.
        if nombre=='-':
            nomweb=''
        else:
            nomweb=nombre
        if apellido1=='-':
            ap1web=''
        else:
            ap1web=apellido1
        if apellido2=='-':
            ap2web=''
        else:
            ap2web=apellido2
            
#With the 3 fields submitted (name, surname1, surname2), we run the programs "busqueda" and "apellidos" to retrieve relevant data from the SQL database
#(see buscar13.py and apellidos13.py).   
        result=busqueda(nomweb,ap1web,ap2web)
        apresult=apellidos(nomweb,ap1web,ap2web)

#Load the HTML template with the data stored in the variables result and apresult.
        return render_template("resultados.html",length=len(result[0]),sumarios=result[0],links=result[1],fondo=result[2],titulo=result[3],total=result[4],apresult=apresult[0],apresult2=apresult[6],nomapresult=apresult[1],nomapresult2=apresult[2],sug1=apresult[3],sug2=apresult[4],sug3=apresult[5],nom=nombre.capitalize(),ap1=apellido1.capitalize(),ap2=apellido2.capitalize(),nomweb=nomweb.capitalize(),ap1web=ap1web.capitalize(),ap2web=ap2web.capitalize())

#This code allows us to run a new search with a new given full name using the navigation bar (POST). Again, we need to remove any apostrophe to avoid issues with the SQL. 
    nombrenew=request.form["nombrenew"].replace("'","")
    apellido1new=request.form["apellido1new"].replace("'","")
    apellido2new=request.form["apellido2new"].replace("'","")

#Once the search is ran, replace any blanks with "-" to update the URL.
    if nombrenew=='':
        nombrenew='-'
    if apellido1new=='':
        apellido1new='-'
    if apellido2new=='':
        apellido2new='-'
#Redirect the user to the new inputted name's URL (https://buscar.combatientes.es/resultados/"Name"/"Surname1"/"Surname2")
    return redirect('/resultados/{}/{}/{}'.format(nombrenew,apellido1new,apellido2new))

###################################################################################################################################################################################
### Type 2 Search: When a Type 2 search is used, the user is redirected to the URL https://buscar.combatientes.es/termino/"Name_or_Surname". This helps in sharing              ###
### the results externally, saving them for later, or even carry out a direct search by modifying the URL.                                                                      ###
###################################################################################################################################################################################

@app.route('/termino/<termino>', methods=["GET", "POST"])
def general(termino):
    if request.method=="GET":
#We use the "Name_or_Surname" (termino) to run a search using the program bus10.py.
        apresult=bus10(termino)
#Once the results are retrieved, convert a possible blank into "-" to avoid an error in the URL.
        if termino=='':
            termino='-'
#Redirect the user to the new inputted name_or_surname's URL (https://buscar.combatientes.es/termino/"Name_or_surname")
        return render_template("resultados3.html",nom=zip(apresult[0],apresult[1],apresult[6]),ap1=zip(apresult[2],apresult[3],apresult[7]),ap2=zip(apresult[4],apresult[5],apresult[8]),term=termino.capitalize(),sug1=apresult[9],sug2=apresult[10],sug3=apresult[11])

#Code for new search.
    nombrenew=request.form["nombrenew"].replace("'","")
    apellido1new=request.form["apellido1new"].replace("'","")
    apellido2new=request.form["apellido2new"].replace("'","")
    
    if nombrenew=='':
        nombrenew='-'
    if apellido1new=='':
        apellido1new='-'
    if apellido2new=='':
        apellido2new='-'
    if nombrenew=="-" and apellido1new =="-" and apellido2new !="-":
        return redirect('/termino/{}'.format(apellido2new))
    if nombrenew=="-" and apellido2new=="-" and apellido1new !="-":
        return redirect('/termino/{}'.format(apellido1new))
    if apellido1new=="-" and apellido2new=="-" and nombrenew !="-":
        return redirect('/termino/{}'.format(nombrenew))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombrenew,apellido1new,apellido2new))


###################################################################################################################################################################################
### Type 3 Search: When a Type 3 search is used, the user is redirected to the URL https://buscar.combatientes.es/busqueda/"Search term". This helps in sharing                 ###
### the results externally, saving them for later, or even carry out a direct search by modifying the URL.                                                                      ###
###################################################################################################################################################################################

@app.route('/busqueda/<busqueda>', methods=["GET", "POST"])
def btotal(busqueda):
    if request.method=="GET":
#We use the search term (busqueda) to run the program btot.py.
        apresult=btot(busqueda)
#Redirect the user to the results page.
        return render_template("resultadosbtot.html",nom=zip(apresult[0],apresult[1],apresult[2],apresult[3]),total=apresult[4],term=busqueda)

#Code for new search.
    btotnew=request.form["btotnew"].replace("'","")
  
#In case the search isn't filled out, replaced the blank space with "NULL" to avoid an error in the URL
    if btotnew=='':
        btotnew='NULL'
    return redirect('/busqueda/{}'.format(btotnew))

###################################################################################################################################################################################
### Sub-pages. This is the "About" page. In addition to loading the information, it also allows the user to directly input the search terms for the Type 1 search               ###
### (Name and Surnames). The description of how this works will be provided here, but won't be repeated for every single sub-page, as it uses the same method.                  ###
###################################################################################################################################################################################
@app.route("/Info/", methods=["GET", "POST"])
def info():
    if request.method=="GET":
        return render_template("info.html")

#Again, we remove the apostrophes that may be inputed by the user to prevent errors with the SQL portion of the code. 
    nombre=request.form["nombre"].replace("'","")
    apellido1=request.form["apellido1"].replace("'","")
    apellido2=request.form["apellido2"].replace("'","")

#And again, once we have gathered the results, we replace any empty fields with a "-" to use directly in the URL (https://buscar.combatientes.es/"Name"/"Surname1"/"Surname2").
    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))
  
#############################
### Sub-pages. "Sources". ###
#############################  
@app.route("/Fuentes/", methods=["GET", "POST"])
def fuentes():
    if request.method=="GET":
        return render_template("fuentes.html")

    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

##############################
### Sub-pages. "Tutorial". ###
############################## 
@app.route("/Tutorial/", methods=["GET", "POST"])
def tutorial():
    if request.method=="GET":
        return render_template("tutorial.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

##############################
### Sub-pages. "Contact".  ###
############################## 
@app.route("/Contacto/", methods=["GET", "POST"])
def contacto():
    if request.method=="GET":
        return render_template("contacto.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

###########################################
### Sub-pages. "Brunete en la Memoria". ###
########################################### 
@app.route("/Brunete_en_la_Memoria/", methods=["GET", "POST"])
def brunete():
    if request.method=="GET":
        return render_template("brunete.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

####################################################
### Sub-pages. "Tribunal Militar Territorial 1". ###
####################################################
@app.route("/TMT1/", methods=["GET", "POST"])
def tmt1():
    if request.method=="GET":
        return render_template("tmt1.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

####################################################
### Sub-pages. "Tribunal Militar Territorial 4". ###
####################################################
@app.route("/TMT4/", methods=["GET", "POST"])
def tmt4():
    if request.method=="GET":
        return render_template("tmt4.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

####################################################
### Sub-pages. "Tribunal Militar Territorial 3". ###
####################################################
@app.route("/TMT3/", methods=["GET", "POST"])
def tmt3():
    if request.method=="GET":
        return render_template("tmt3.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

#######################################################
### Sub-pages. "Batallon de Soldados Trabajadores". ###
#######################################################
@app.route("/BDST/", methods=["GET", "POST"])
def bdst():
    if request.method=="GET":
        return render_template("bdst.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

###########################################
### Sub-pages. "Prisioneros de Guerra". ###
###########################################
@app.route("/PDG/", methods=["GET", "POST"])
def pdg():
    if request.method=="GET":
        return render_template("prisioneros_de_guerra.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

################################################
### Sub-pages. "Boletin Oficial del Estado". ###
################################################
@app.route("/BOE/", methods=["GET", "POST"])
def boe():
    if request.method=="GET":
        return render_template("boe.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))


#########################################################
### Sub-pages. "Comision Central de Examen de Penas". ###
#########################################################
@app.route("/CCEP/", methods=["GET", "POST"])
def ccep():
    if request.method=="GET":
        return render_template("ccep.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

###################################################################
### Sub-pages. "Archivo de la Real Chancilleria de Valladolid". ###
###################################################################
@app.route("/ACV/", methods=["GET", "POST"])
def acv():
    if request.method=="GET":
        return render_template("chancilleria.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))


################################################
### Sub-pages. "Archivo Historico Nacional". ###
################################################
@app.route("/AHN/", methods=["GET", "POST"])
def ahn():
    if request.method=="GET":
        return render_template("ahn.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    #Una vez tenemos los resultados, rellenar los espacios en blanco con - para que funcione cualquier entrada en la barra de direccion.
    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

#################################################
### Sub-pages. "Responsabilidades Politicas". ###
#################################################
@app.route("/CDMHrp/", methods=["GET", "POST"])
def respol():
    if request.method=="GET":
        return render_template("respol.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))
      
###################################
### Sub-pages. "Causa General". ###
###################################
@app.route("/CausaGen/", methods=["GET", "POST"])
def causagen():
    if request.method=="GET":
        return render_template("causagen.html")
    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))

######################################
### Sub-pages. "Document request". ###
######################################
@app.route("/Documento/", methods=["GET"])
def docoff():
    return render_template("documento.html")



###################################################
### Sub-pages. "People incarcerated in Murcia". ###
###################################################
@app.route("/Presos_Murcia/", methods=["GET", "POST"])
def presmurcia():
    if request.method=="GET":
        return render_template("murcia.html")

    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))


##########################################
### Sub-pages. "Refugees from Toledo". ###
##########################################
@app.route("/Evacuados_Toledo/", methods=["GET", "POST"])
def reftoledo():
    if request.method=="GET":
        return render_template("refugiados_toledo.html")

    nombre=request.form["nombrenew"].replace("'","")
    apellido1=request.form["apellido1new"].replace("'","")
    apellido2=request.form["apellido2new"].replace("'","")

    if nombre=='':
        nombre='-'
    if apellido1=='':
        apellido1='-'
    if apellido2=='':
        apellido2='-'
    if nombre=="-" and apellido1 =="-" and apellido2 !="-":
        return redirect('/termino/{}'.format(apellido2))
    if nombre=="-" and apellido2=="-" and apellido1 !="-":
        return redirect('/termino/{}'.format(apellido1))
    if apellido1=="-" and apellido2=="-" and nombre !="-":
        return redirect('/termino/{}'.format(nombre))
    else:
        return redirect('/resultados/{}/{}/{}'.format(nombre,apellido1,apellido2))
