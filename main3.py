from flask import Flask,render_template,request,redirect
from flask.globals import request
import os
import random
import threading
import datetime
import time

from flask.helpers import locked_cached_property

app = Flask(__name__)

dato1=0
dato2=0
dato3=0
@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/datos')
def datos():
    user= {'nombre' : 'Cristian'}
    return render_template('datos.html',title='Titulo Personalizado',user=user)

@app.route('/menu',methods=["POST"])
def validar():
    if request.method=="POST":
        usuario=request.form['usuario']
        password=request.form['password']
        resultado=True
        resultado=verificar(usuario,password)
        if resultado ==True:
            return render_template('menu.html',title='Sistema DABM')
        else:
            resultado=False
            return redirect("/")

@app.route('/Rangos',methods=["POST"])   
def Rango():
    if request.method == "POST":
        minHipo=request.form["minHipo"]
        maxHipo=request.form["maxHipo"]
        minNormal=request.form["minNormal"]
        maxNormal=request.form["maxNormal"] 
        minFiebre=request.form["minFiebre"]
        maxFiebre=request.form["maxFiebre"]
        cambiarRangos(minHipo,maxHipo,minNormal,maxNormal,minFiebre,maxFiebre)

        return render_template('menu.html')

def cambiarRangos(minHipo,maxHipo,minNormal,maxNormal,minFiebre,maxFiebre):
    directorio=os.path.dirname(__file__)        #se abre y lee el archivo de texto de "parametros.cvs"
    nombrearchivo="bd/parametros.csv"
    ruta=os.path.join(directorio,nombrearchivo)

    f=open(ruta,"w")
    datos="hipotermia"+";"+minHipo+";"+maxHipo+"\n"+"normal"+";"+minNormal+";"+maxNormal+"\n"+"fiebre"+";"+minFiebre+";"+maxFiebre+"\n"
    f.write(datos)
    f.close()

def sensor1():
    global dato1
    dato1 = random.randint(20,45)
    hora = datetime.datetime.now()
    registro = str(dato1) + ";" + str(hora)+ "\n"
    print(registro) 
    time.sleep(1)

    directorio = os.path.dirname(__file__)
    archivo = "bd/sensor1.csv"
    storage = os.path.join(directorio,archivo)

    f=open(storage,"a")
    f.write(registro)
    f.close

def sensor2():
    global dato2
    dato2 = random.randint(20,45)
    hora = datetime.datetime.now()
    registro = str(dato2) + ";" + str(hora)+ "\n"
    print(registro) 
    time.sleep(1)

    directorio = os.path.dirname(__file__)
    archivo = "bd/sensor2.csv"
    storage = os.path.join(directorio,archivo)

    f=open(storage,"a")
    f.write(registro)
    f.close    

def sensor3():
    global dato3
    dato3 = random.randint(20,45)
    hora = datetime.datetime.now()
    registro = str(dato3) + ";" + str(hora)+ "\n"
    print(registro) 
    time.sleep(1)

    directorio = os.path.dirname(__file__)
    archivo = "bd/sensor3.csv"
    storage = os.path.join(directorio,archivo)

    f=open(storage,"a")
    f.write(registro)
    f.close

@app.route('/monitor')
def monitor():
    h1=threading.Thread(target=sensor1)
    h1.daemon = True
    h2 = threading.Thread(target=sensor2)
    h2.daemon = True
    h3 = threading.Thread(target=sensor3)
    h3.daemon = True

    h1.start()
    h2.start()
    h3.start()

    #consultar archivo de parametros
    datos=getDatos()
    # obtener lectura
    lecturas=[dato1,dato2,dato3]
    #lectura=random.randint(int(datos[0][1]),int(datos[2][2])) #se generan los valores aleatorios dentro del rango de parametros establecidos
    # enviar a la interfaz
    
    colores=[]
    for lectura in lecturas:
        color=0
        if lectura >= int(datos[0][1]) and lectura <= int(datos[0][2]):
            color=1 
        if lectura >= int(datos[1][1]) and lectura <= int(datos[1][2]):
            color=2 
        if lectura>= int(datos[2][1]) and lectura <= int(datos[2][2]):
            color=3
        colores.append(color)
    return render_template("/monitor2.html",datos=datos,lecturas=lecturas,colores=colores)
        
def verificar(usuario,password):
    directorio=os.path.dirname(__file__)        #se abre y lee el archivo de texto de "users.cvs"
    nombrearchivo="bd/users.csv"
    ruta=os.path.join(directorio,nombrearchivo)

    f= open(ruta,"r")
    lineas=f.readlines()        #leemos las lineas del archivo de texto
    f.close()
    datos=[]                    #lista donde vamos a almacenar cada fila del  archivo de texto
    for l in lineas:
        l=l.replace("\n","")
        l=l.split(";")
        datos.append(l)

    for d in datos:
        if ((d[0]==usuario) and (d[1]==password)):
            return True

@app.route("/Rangos")
def rangos():
    pass
    
def getDatos():
    directorio=os.path.dirname(__file__)
    nombrearchivo="bd/parametros.csv"
    ruta=os.path.join(directorio,nombrearchivo)

    f= open(ruta,"r")
    lineas=f.readlines()
    f.close()
    datos=[]
    for l in lineas:
        l=l.replace("\n","")
        l=l.split(";")
        datos.append(l)
    return datos
        
@app.route("/config")
def config():
    return render_template("config.html")


if __name__=="__main__":
    app.run(debug=True)