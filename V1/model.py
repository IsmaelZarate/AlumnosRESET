from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

db = SQLAlchemy()


class Carreras(db.Model):
    __tablename__ = 'carreras'
    idCarrera = db.Column(Integer, primary_key=True)
    nombre = db.Column(String, nullable=False)
    siglas = db.Column(String, nullable=False)
    creditos = db.Column(Integer, nullable=False)
    planEstudios = db.Column(String, nullable=False)
    especialidad = db.Column(String, nullable=False)
    estatus = db.Column(String, default='A')

    def consultaGeneral(self):  # select * from carreras
        lista = self.query.all()
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            if len(lista) > 0:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "Listado de opciones de Carreras."
                respuesta["opciones"] = [o.to_json() for o in lista]
            else:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "No hay carreras registradas"
                respuesta["carreras"] = []
        except:
            respuesta["estatus"] = "Error"
            respuesta["mensaje"] = "Problemas de al ejecutar la consulta de carreras"
        return respuesta

    def to_json(self):
        to_json = {"idCarrera": self.idCarrera,
                   "nombre": self.nombre,
                   "siglas": self.siglas,
                   "creditos": self.creditos,
                   "planEstudios": self.planEstudios,
                   "especialidad": self.especialidad,
                   "estatus": self.estatus

                   }

        return to_json

    def insertarCarrera(self, idCarrera, nombre, siglas, creditos, planEstudios, especialidad, estatus):
        carrerasadd = Carreras(idCarrera=idCarrera, nombre=nombre, siglas=siglas, creditos=creditos,
                               planEstudios=planEstudios,
                               especialidad=especialidad, estatus=estatus)

        db.session.add(carrerasadd)
        db.session.commit()

        respuesta = {"estatus": "EXITO :D", "mensaje": "Agregado Exitosamente"}
        return respuesta

    def to_json(self):
        o_json = {"idCarrera": self.idCarrera,
                  "nombre": self.nombre,
                  "siglas": self.siglas,
                  "creditos": self.creditos,
                  "planEstudios": self.planEstudios,
                  "especialidad": self.especialidad,
                  "estatus": self.estatus

                  }
        return o_json

    def actualizarCarrera(self, idCarrera, nombre, siglas, creditos, planEstudios, especialidad, estatus):
        carrera = Carreras.query.get(idCarrera)
        if carrera:
            carrera.nombre = nombre
            carrera.siglas = siglas
            carrera.creditos = creditos
            carrera.planEstudios = planEstudios
            carrera.especialidad = especialidad
            carrera.estatus = estatus

            db.session.commit()

            respuesta = {
                "estatus": "ok",
                "mensaje": "Carrera actualizada"
            }
        else:
            respuesta = {
                "estatus": "error",
                "mensaje": "No se encuentra la carrera"
            }
        return respuesta

    def eliminarCarrera(self, idCarrera):
        carreraDE = Carreras.query.get(idCarrera)
        if carreraDE:
            db.session.delete(carreraDE)
            db.session.commit()

            respuesta = {
                "estatus": "ok",
                "mensaje": "Carrera eliminada"
            }
        else:
            respuesta = {
                "estatus": "error",
                "mensaje": "No se encuentra la carrera"
            }

        return respuesta


class Opcion(db.Model):
    __tablename__ = 'opciones'
    idOpcion = db.Column(Integer, primary_key=True)
    nombre = db.Column(String, nullable=False)
    descripcion = db.Column(String)
    estatus = db.Column(String, default='A')


class Solicitud(db.Model):
    __tablename__ = 'Solicitudes'
    idSolicitud = db.Column(Integer, primary_key=True)

    # Metodo que invoca el procedimienton almacenado sp_registrar_solicitud
    def agregar(self, json):
        respuesta = {"estatus": "", "mensaje": ""}
        db.session.execute('call sp_registrar_solicitud(:tituloProyecto,:opcion,:alumno,@p_estatus,@p_mensaje)', json)
        db.session.commit()
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def editar(self, json):
        respuesta = {"estatus": "", "mensaje": ""}
        db.session.execute(
            'call sp_modificar_solicitud(:idSolicitud,:tituloProyecto,:estatus,:opcion,:administrativo,:tipoUsuario,@p_estatus,@p_mensaje)',
            json)
        db.session.commit()
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def eliminar(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        json = {"idSolicitud": id}
        db.session.execute('call sp_eliminar_solicitud(:idSolicitud,@p_estatus,@p_mensaje)', json)
        db.session.commit()
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def consultaGeneral(self):
        respuesta = {"estatus": "", "mensaje": "", "solicitudes": ""}
        resultado = db.session.execute("select * from vsolicitudes").fetchall()
        lista = []
        for reg in resultado:
            lista.append(self.to_json(reg))
        if len(lista) > 0:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "Listado de solicitudes"
            respuesta["solicitudes"] = lista
        else:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "No hay solicitudes registradas"
            respuesta["solicitudes"] = lista
        return respuesta

    def consultaIndividual(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        param = {"id": id}
        resultado = db.session.execute("select * from vsolicitudes where idSolicitud=:id", param).fetchall()
        if resultado:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "Listado de la solicitud con id:" + str(id)
            respuesta["solicitud"] = [self.to_json(row) for row in resultado]
        else:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "No se encuentra registrada la solicitud con id:" + str(id)
        return respuesta

    def consultarSolicitudesAlumnos(self, noControl):
        respuesta = {"estatus": "", "mensaje": ""}
        param = {"noControl": noControl}
        resultado = db.session.execute("select * from vAlumnos where noControl=:noControl", param).fetchone()
        if resultado:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "Listado de la solicitud del alumno con NC:" + str(noControl)
            respuesta["solicitud"] = self.to_json(resultado)
        else:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "No se encuentra registrada la solicitud del alumno con NC:" + str(noControl)
        return respuesta

    def to_json(self, fila):
        solicitud = {"administrativo": "", "alumno": "", "carrera": "", "estatus": "", "fechaAtencion": "",
                     "fechaRegistro": "", "id": "", "opcion": "", "proyecto": ""}
        solicitud["administrativo"] = {"id": fila[10], "nombre": fila[11]}
        solicitud["alumno"] = {"id": fila[1], "NC": fila[2], "nombre": fila[3]}
        solicitud["carrera"] = {"id": fila[12], "nombre": fila[13]}
        solicitud["estatus"] = fila[7]
        solicitud["fechaAtencion"] = fila[6]
        solicitud["fechaRegistro"] = fila[5]
        solicitud["id"] = fila[0]
        solicitud["opcion"] = {"id": fila[8], "nombre": fila[9]}
        solicitud["proyecto"] = fila[4]
        return solicitud


class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    idUsuario = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(100), nullable=False)
    sexo = db.Column(String(1), nullable=False)
    telefono = db.Column(String(12), nullable=False)
    email = db.Column(String(100), nullable=False)
    password = db.Column(String(20), nullable=False)
    tipo = db.Column(String(1), nullable=False)
    estatus = db.Column(String(1), nullable=False)

    def comprobarCredenciales(self, email, password):
        user = self.query().filter(Usuario.email == email, Usuario.password == password, Usuario.estatus == 'A').firts()
        if user:
            return user
        else:
            return None
