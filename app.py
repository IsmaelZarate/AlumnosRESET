from flask import Flask, jsonify, request
from V1.model import Opcion, db, Solicitud, Carreras
from V1.SolicitudesBPV1 import solicitudBP

from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)

app.register_blueprint(solicitudBP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Zarate15@/ServiciosCarreras'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

users = {
    "ismael": {"password": generate_password_hash("12345"), "role": "consult"},
    "miguel": {"password": generate_password_hash("123456"), "role": "add-consult"}
}





@app.route('/', methods=['GET'])
def init():
    return {"mensaje": "Escuchando el Servicio REST de Solicitudes"}


# Rutta para el listado general de Carreras
@app.route('/Carreras/V1', methods=['GET'])
def listadoSolicitudes():
    carreras = Carreras()
    return carreras.consultaGeneral()


# Ruta para el listado indvidual de solicitudes en base al id de la solicitud
@app.route('/Solicitudes/v1/<int:id>', methods=['GET'])
def listarSolicitud(id):
    solicitud = Solicitud()
    return solicitud.consultaIndividual(id)


@app.route('/Agregar/V1', methods=['POST'])
def AgregarCarrera():
    idCarrera = request.json.get('idCarrera')
    nombre = request.json.get('nombre')
    siglas = request.json.get('siglas')
    creditos = request.json.get('creditos')
    planEstudios = request.json.get('planEstudios')
    especialidad = request.json.get('especialidad')
    estatus = request.json.get('estatus')

    if idCarrera is None or nombre is None or siglas is None or creditos is None or planEstudios is None or especialidad is None or estatus is None:
        return jsonify({"mensaje": "Campos incompletos"}), 400

    carrerasAdd = Carreras()

    respuesta = carrerasAdd.insertarCarrera(idCarrera, nombre, siglas, creditos, planEstudios, especialidad, estatus)
    return jsonify(respuesta)


# Modificafr carrera
@app.route('/Update/V1/<int:idCarrera>', methods=['PUT'])
def editarCarrera(idCarrera):
    carrerasUpdate = Carreras()
    if request.method == 'PUT':
        nombre = request.json.get('nombre')
        siglas = request.json.get('siglas')
        creditos = request.json.get('creditos')
        planEstudios = request.json.get('planEstudios')
        especialidad = request.json.get('especialidad')
        estatus = request.json.get('estatus')

        if idCarrera is None or nombre is None or siglas is None or creditos is None or planEstudios is None or especialidad is None or estatus is None:
            return jsonify({"mensaje": "Campos incompletos"}), 400

        carrera = Carreras()
        respuesta = carrera.actualizarCarrera(idCarrera, nombre, siglas, creditos, planEstudios, especialidad, estatus)

        return jsonify(respuesta)


# Rutta para el listado general de Carreras
@app.route('/Delete/V1/<int:idCarrera>', methods=['DELETE'])
def deleteCarrera(idCarrera):
    if request.method == 'DELETE':
        carreraDE = Carreras()
        respuesta = carreraDE.eliminarCarrera(idCarrera)

    return jsonify(respuesta)


# Ruta para agregar una solicitud
@app.route('/Solicitudes/v1', methods=['POST'])
def agregarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.agregar(data)


# Ruta para editar los datos de una solicitud
@app.route('/Solicitudes/v1', methods=['PUT'])
def editarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.editar(data)


# Ruta para eliminar una solicitud
@app.route('/Carreras/V1/<int:id>', methods=['DELETE'])
def eliminarCarrera(id):
    carreras = Carreras()
    return carreras.eliminarCarrera(id)


# Ruta para el listado de las opciones disponibles para titulación
@app.route('/opciones', methods=['GET'])
def consultaOpciones():
    # try:
    opcion = Opcion()
    return jsonify(opcion.consultaGeneral())


# except:
# respuesta = {"estatus": "Error", "mensaje": "Recurso no disponible, contacta al administrador del servicio"}
# return respuesta

# Manipulaciones de errores
@app.errorhandler(404)
def errorinterno(e):
    respuesta = {"estatus": "Error", "mensaje": "Recurso no disponible, contacta al administrador del servicio"}
    return respuesta


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
