from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all, fetch_one
from datetime import datetime

routes_asistencia = Blueprint('routes_asistencia', __name__)

@routes_asistencia.route('/confirmar_asistencia', methods=['POST'])
def confirmar_asistencia():
    data = request.get_json()
    id_docente = data['id_docente']
    aula = data['aula']
    fecha_registro = datetime.now()

    # Obtener los datos del docente
    query_docente = "SELECT * FROM docentes WHERE id = %s"
    docente = fetch_one(query_docente, (id_docente,))

    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    # Obtener los estudiantes registrados con este docente
    query_estudiantes = "SELECT * FROM registro_estudiantes WHERE id_docente = %s"
    estudiantes = fetch_all(query_estudiantes, (id_docente,))

    if not estudiantes:
        return jsonify({'error': 'No hay estudiantes registrados para este docente'}), 404

    # Insertar los datos en la tabla asistencias
    for estudiante in estudiantes:
        query_asistencia = '''
        INSERT INTO asistencias (cedula_estudiante, nombre_estudiante, apellido_estudiante, correo_estudiante, carrera_estudiante,
                                 numero_maquina_estudiante, cedula_docente, nombre_docente, apellido_docente, correo_docente,
                                 materia, semestre, paralelo, aula, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (estudiante['cedula'], estudiante['nombre_estudiante'], estudiante['apellido_estudiante'], estudiante['correo'], estudiante['carrera'],
                  estudiante['numero_maquina'], docente['cedula'], docente['nombre'], docente['apellido'],
                  docente['correo'], estudiante['materia'], docente['semestre'], docente['paralelo'], aula, fecha_registro)
        execute_query(query_asistencia, params)

    return jsonify({'message': 'Asistencia confirmada y registrada exitosamente'}), 201
