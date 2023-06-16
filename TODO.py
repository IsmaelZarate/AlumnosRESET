
class Opcion(db.Model):
    __tablename__ = 'opciones'
    idOpcion = db.Column(Integer, primary_key=True)
    nombre = db.Column(String, nullable=False)
    descripcion = db.Column(String)
    estatus = db.Column(String, default='A')

    def consultaGeneral(self):  # select * from opciones
        lista = self.query.all()
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            if len(lista) > 0:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "Listado de opciones de titulacion."
                respuesta["opciones"] = [o.to_json() for o in lista]
            else:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "No hay opciones registradas"
                respuesta["opciones"] = []
        except:
            respuesta["estatus"] = "Error"
            respuesta["mensaje"] = "Problemas de al ejecutar la consulta de opciones"
        return respuesta

    def to_json(self):
        to_json = {"idOpcion": self.idOpcion,
                   "nombre": self.nombre,
                   "descripcion": self.descripcion
                   }
        return to_json


class Carreras(db.Model):
    __tablename__ = 'carreras'
    idCarrera = db.Column(Integer, primary_key=True)
    idAdministrativo = db.Column(Integer, db.ForeignKey("carreras.idAdministrativo"))
    nombre = db.Column(String, nullable=False)
    siglas = db.Column(String, nullable=False)
    creditos = db.Column(Integer, nullable=False)
    planEstudios = db.Column(String, nullable=False)
    especialidad = db.Column(String, nullable=False)
    estatus = db.Column(String, default='A')


class Alumno(db.Model):
    __tablename__ = 'valumnos'
    idAlumno = db.Column(Integer, primary_key=True)
    noControl = db.Column(String, nullable=False)
    nombre_alumno = db.Column(String, nullable=False)
    sexo = db.Column(String, nullable=False)
    creditos = db.Column(String, nullable=False)
    anioEgreso = db.Column(Date, nullable=False)
    telefono = db.Column(String, nullable=False)
    email = db.Column(String, nullable=False)
    password = db.Column(String, nullable=False)
    idCarrera = db.Column(Integer, db.ForeignKey("carreras.idCarrera"))
    nombre_carrera = db.Column(String, db.ForeignKey("carreras.nombre_carrera"))
    estatus = db.Column(String, nullable=False)

    def eliminarAlumnos(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        json = {"idAlumno": id}
        db.session.execute('call sp_eliminar_alumno(:idAlumno,@p_estatus,@p_mensaje)', json)
        db.session.commit()
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def consultaIndividual(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        param = {"id": id}
        resultado = db.session.execute("select * from valumnos where idAlumno=:id", param).fetchall()
        if resultado:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "Listado de la solicitud con id:" + str(id)
            respuesta["alumno"] = [self.to_json(row) for row in resultado]
        else:
            respuesta["estatus"] = "OK"
            respuesta["mensaje"] = "No se encuentra registrado el alumno con id :" + str(id)
        return respuesta

    def consultaGeneralAlumnos(self):
        lista = self.query.all()
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            if len(lista) > 0:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "Listado de alumnos ."
                respuesta["alumno"] = [o.to_json() for o in lista]
            else:
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "No hay alumnos registrados"
                respuesta["alumno"] = []
        except:
            respuesta["estatus"] = "Error"
            respuesta["mensaje"] = "Problemas de al ejecutar la consulta de alumnos"
        return respuesta

    def insertarAlumno(self, idAlumno, noControl, nombre_alumno, sexo, creditos, anioEgreso, telefono, email, idCarrera,
                       nombre_carrera, estatus):
        alumno = Alumno(idAlumno=idAlumno, noControl=noControl, nombre_alumno=nombre_alumno, sexo=sexo,
                        creditos=creditos, anioEgreso=anioEgreso, telefono=telefono, email=email, idCarrera=idCarrera,
                        nombre_carrera=nombre_carrera, estatus=estatus)

        db.session.add(alumno)
        db.session.commit()

        respuesta: {"estatus": "Exito", "mensaje": "Se inserto chido"}

        return respuesta

    def to_json(self):
        to_json = {"idAlumno": self.idAlumno,
                   "noControl": self.noControl,
                   "nombre_alumno": self.nombre_alumno,
                   "sexo": self.sexo,
                   "creditos": self.creditos,
                   "anioEgreso": self.anioEgreso,
                   "telefono": self.telefono,
                   "email": self.email,
                   "idCarrera": self.idCarrera,
                   "nombre_carrera": self.nombre_carrera,
                   "estatus": self.estatus

                   }
        return to_json


class Solicitud(db.Model):
    __tablename__ = 'Solicitudes'
    idSolicitud = db.Column(Integer, primary_key=True)
    fechaRegistro = db.Column(Date, nullable=False)
    fechaAtencion = db.Column(Date, nullable=True)
    tituloProyecto = db.Column(String, nullable=False)
    estatus = db.Column(String, nullable=False)
    idOpcion = db.Column(Integer, db.ForeignKey("opciones.idOpcion"))
    idAdministrativo = db.Column(Integer, db.ForeignKey("administrativos.idAdministrativo"))
    idAlumno = db.Column(Integer, db.ForeignKey("alumnos.idAlumno"))

    # Metodo que invoca el procedimienton almacenado sp_registrar_solicitud
    def agregar(self, json):
        respuesta = {"estatus": "", "mensaje": ""}
        db.session.execute('call sp_registrar_solicitud(:tituloProyecto,:idOpcion,:idAlumno,@p_estatus,@p_mensaje)',
                           json)
        db.session.commit()
        salida = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
        respuesta['estatus'] = salida[0]
        respuesta['mensaje'] = salida[1]
        return respuesta

    def editar(self, json):
        respuesta = {"estatus": "", "mensaje": ""}
        db.session.execute(
            'call sp_modificar_solicitud(:idSolicitud,:tituloProyecto,:estatus,:idOpcion,:idAdministrativo,@p_estatus,@p_mensaje)',
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
        resultado = db.session.execute("select * from valumnos where noControl=:noControl", param).fetchone()
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





APP.PY



@app.route('/Alumnos/V1', methods=['POST'])
def agregarAlumno():
    idAlumno = request.json.get('idAlumno')
    noControl = request.json.get('noControl')
    nombre_alumno = request.json.get('nombre_alumno')
    sexo = request.json.get('sexo')
    creditos = request.json.get('creditos')
    anioEgreso = request.json.get('anioEgreso')
    telefono = request.json.get('telefono')
    email = request.json.get('email')
    password = request.json.get('password')
    idCarrera = request.json.get('idCarrera')
    nombre_carrera = request.json.get('nombre_carrera')
    estatus = request.json.get('estatus')

    if idAlumno is None or noControl is None or nombre_alumno is None or sexo is None or creditos is None or anioEgreso is None or telefono is None or email is None or password is None or idCarrera is None or nombre_carrera is None or estatus is None:
        return jsonify({"estatus": "campos incompletos"}), 400
    alumno = Alumno()
    respuesta = alumno.insertarAlumno(idAlumno,noControl,nombre_alumno,sexo,creditos,anioEgreso,telefono,email,idCarrera,nombre_carrera,estatus)
    return jsonify(respuesta)


@app.route('/Usuarios/Alumnos/V1', methods=['GET'])
def consultaAlumnos():
    alumno = Alumno()
    return alumno.consultaGeneralAlumnos()


# Rutta para el listado general de solicitudes
@app.route('/Solicitudes/V1', methods=['GET'])
def listadoSolicitudes():
    solicitud = Solicitud()
    return solicitud.consultaGeneral()


# Ruta para el listado indvidual de solicitudes en base al id de la solicitud
@app.route('/Solicitudes/V1/<int:id>', methods=['GET'])
def listarSolicitud(id):
    solicitud = Solicitud()
    return solicitud.consultaIndividual(id)


# Ruta para agregar una solicitud
@app.route('/Solicitudes/V1', methods=['POST'])
def agregarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.agregar(data)


# Ruta para editar los datos de una solicitud
@app.route('/Solicitudes/V1', methods=['PUT'])
def editarSolicitud():
    solicitud = Solicitud()
    data = request.get_json()
    return solicitud.editar(data)


# Ruta para eliminar una solicitud
@app.route('/Solicitudes/V1/<int:id>', methods=['DELETE'])
def eliminarSolicitud(id):
    solicitud = Solicitud()
    return solicitud.eliminar(id)


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
    respuesta = {"estatus": "Error", "mensaje": "Recurso no disponible, contacta al administrador del servicio jiji"}
    return respuesta


@app.route('/Solicitudes/V1/alumno/<int:noControl>', methods=['GET'])
def consultarSolicitudesAlumnos(noControl):
    sol = Solicitud()
    return sol.consultarSolicitudesAlumnos(noControl)
