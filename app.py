from flask import Flask, jsonify, request
# from V1.SolicitudesBPV1 import solicitudBP

from V1.model import Alumnos, db, Carrera

app = Flask(__name__)
# app.register_blueprint(solicitudBP)
# app.register_blueprint(solicitudBPV2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola@localhost/servicioAlumno'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/', methods=['GET'])
def init():
    return {"mensaje": "Escuchando el Servicio REST de Solicitudes"}


@app.route('/Usuarios/Alumnos', methods=['GET'])
def listarAlumnos():
    alumno = Alumnos()
    return jsonify(alumno.consultarAlumnos())


@app.route('/Usuarios/AlumnosAg', methods=['POST'])
def AgregarAlumnos():
    idAlumno = request.json.get('idAlumno')
    nombre = request.json.get('nombre'),
    anioIngreso = request.json.get('anioIngreso'),
    anioEgreso = request.json.get('anioEgreso'),
    sexo = request.json.get('sexo'),
    telefono = request.json.get('telefono'),
    correo = request.json.get('correo'),
    passwords = request.json.get('passwords'),
    nControl = request.json.get('nControl'),
    tipo = request.json.get('tipo'),
    estatus = request.json.get('estatus'),
    idCarrera = request.json.get('idCarrera')

    alumno = Alumnos()
    respuesta = alumno.insertarAlumno(idAlumno, nombre, anioIngreso, anioEgreso, sexo, telefono, correo, passwords,
                                      nControl, tipo, estatus, idCarrera)
    return jsonify(respuesta)


@app.route('/Usuarios/AlumnosEl/<int:idAlumno>', methods=['DELETE'])
def eliminarAlumno(idAlumno):
    if request.method == 'DELETE':
        alumno = Alumnos()
        respuesta = alumno.eliminarAlumno(idAlumno)
    return jsonify(respuesta)




@app.route('/Usuarios/AlumnosEd/<int:idAlumno>', methods=['PUT'])
def editarAlumno(idAlumno):
    alumno = Alumnos()
    if request.method == 'PUT':
        nombre = request.json.get('nombre')
        anioIngreso = request.json.get('anioIngreso')
        anioEgreso = request.json.get('anioEgreso')
        sexo = request.json.get('sexo')
        telefono = request.json.get('telefono')
        correo = request.json.get('correo')
        paswords = request.json.get('passwords')
        nControl = request.json.get('nControl')
        tipo = request.json.get('tipo')
        estatus = request.json.get('estatus')
        idCarrera = request.json.get('idCarrera')

        if idAlumno is None or nombre is None or anioIngreso is None or anioEgreso is None or sexo is None or telefono is None or correo is None or paswords is None or nControl is None or tipo is None or estatus is None:
            return jsonify({"mensaje": "Campos incompletos"}), 400

        alumno = Alumnos()
        respuesta = alumno.editarAlumno(idAlumno, nombre, anioIngreso, anioEgreso, sexo, telefono, correo,
                                              paswords, nControl, tipo, estatus,idCarrera)

    return jsonify(respuesta)



if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
