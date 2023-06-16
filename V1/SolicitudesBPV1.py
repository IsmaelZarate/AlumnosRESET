from flask import Blueprint, request
from V1.model import Solicitud, Usuario

# from flask_httpauth import HTTPBasicAuth

solicitudBP = Blueprint('SolicitudBP', __name__)


# auth = HTTPBasicAuth()


@solicitudBP.route('/Solicitudes/V1', methods=['GET'])
def listadoSolicitudes():
    solicitud = Solicitud()
    return solicitud.consultaGeneral()


# @auth.verify_password
# def verificarUsuario(username, password):
# u=Usuario()
# user=u.comprobarCredenciales(username, password)
# if user!=None:
#   return user
# else:
#   return False


# @auth.get_user_roles
# def get_user_roles(user):
#   return user.tipo


# @auth.error_handler
# def error_handler():
# return {"estatus": "error", "mensaje": "Accesi no autorizado"}


@solicitudBP.route('/Solicitudes/v1/<int:id>', methods=['GET'])
# @auth.login_required(role='A')
def listarSolicitud(id):
    solicitud = Solicitud()
    return solicitud.consultaIndividual(id)


@solicitudBP.route('/Solicitudes/v1', methods=['POST'])
def agregarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.agregar(data)


@solicitudBP.route('/Solicitudes/v1', methods=['PUT'])
def editarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.editar(data)


@solicitudBP.route('/Solicitudes/evidencias')
def listadoEvidencias():
    respuesta = {"estatus": "200", "mensaje": "Listado de evidencias de las solicitudes"}
    return respuesta


@solicitudBP.route('/Solicitudes/<int:id>', methods=['DELETE'])
def eliminarSolicitud(id):
    respuesta = {"estatus": "200", "mensaje": "Eliminando la solicitud con id:" + str(id)}
    return respuesta


@solicitudBP.route('/Solicitudes/<string:nc>')
def consultarSolicitud(nc):
    respuesta = {"estatus": "200", "mensaje": "Buscando la solicitud que registro el alumno con NC:" + nc}
    return respuesta


@solicitudBP.route('/Solicitudes/v1/alumno/<int:idAlumno>', methods=['GET'])
def consultarSolicitudesAlumnos(idAlumno):
    sol = Solicitud()
    return sol.consultarSolicitudesAlumnos(idAlumno)
