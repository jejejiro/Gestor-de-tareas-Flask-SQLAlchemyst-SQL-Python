from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea
from datetime import datetime # importa la libreria datetime

app = Flask(__name__)

@app.route("/")
def home():
    todasLasTareas = db.session.query(Tarea).all()
    for  i in todasLasTareas:
        print(i)
    dt = datetime.now() # instancia el objeto datetime
    fecha = dt.strftime("%Y-%m-%d") # convierte el objeto daetime a str
    # Se envia la fecha actual en formato str para que se almacene en el formulario por defecto
    return render_template("index.html", listaDeTareas=todasLasTareas, fechaActual=fecha)

@app.route("/crearTarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form["contenidoTarea"], hecha=False, importante=False, fecha=request.form["fechaTarea"])
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tareaHecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    #tarea = db.session.query(Tarea).filter_by(id = int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tareaEliminar/<id>")
def eliminar(id):
    db.session.query(Tarea).filter(Tarea.id == int(id)).delete()
    #tarea = db.session.query(Tarea).filter_by(id = int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

# Ejecuta la funcion de cambiar el booleano de true a false para importante
@app.route("/tareaImportante/<id>")
def importante(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    #importante = db.session.query(Tarea).filter_by(id = int(id)).first()
    tarea.importante = not(tarea.importante)
    db.session.commit()
    return redirect(url_for("home"))

# Reenderiza la pagina donde se realiza la modificacion de la tarea
@app.route("/modificarTarea", methods=["GET"]) # metodo GET obtiene datos de la url
def modificarTarea():
    id = request.args.get('id') # pregunta por el id y lo almacena en una variable
    dt = datetime.now()  # instancia el objeto datetime
    fecha = dt.strftime("%Y-%m-%d") # convierte el objeto datetime a str
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    return render_template("modificarTarea.html", fechaAModificar=fecha, tarea=tarea)

# Ejecuta el cambio hecho en la tarea y lo envia a la base de datos
@app.route("/modificar/<id>", methods=["POST"])
def modificar(id):
    nuevoContenido = request.form["contenidoModoficadoTarea"] # consulta por el contenido modificado
    nuevafecha = request.form["fechaModificadaTarea"] # consulta por la fecha modificada
    tareaModificada = db.session.query(Tarea).filter(Tarea.id == int(id)).first() # busca el objeto en la base de datos
    tareaModificada.contenido = nuevoContenido # cambia el contenido
    tareaModificada.fecha = nuevafecha # cambia la fecha
    db.session.commit() #gurada los cambios
    return redirect(url_for("home"))



if __name__ == "__main__":
    #db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)



