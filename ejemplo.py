from flask import Flask,render_template
from flask.globals import request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/datos')
def datos():
    user= {'nombre' : 'Cristian'}
    return render_template('datos.html',title='Titulo Personalizado',user=user)

@app.route('/validar',methods=["POST"])
def validar():
    if request.method=="POST":
        usuario=request.form['usuario']
        password=request.form['password']

        print(usuario)
        print(password)

        resultado=verificar(usuario,password)

def verificar():
    pass


if __name__=="__main__":
    app.run(debug=True)