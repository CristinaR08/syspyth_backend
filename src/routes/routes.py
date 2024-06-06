from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all, fetch_one

routes = Blueprint('routes', __name__)

#POST

@routes.route('/estudiantes', methods=['POST'])
def add_estudiante():
    new_estudiante = request.json

    print("Datos del estudiante recibidos:", new_estudiante)

    # Validar que los datos del estudiante están presentes
    if not new_estudiante or 'cedula' not in new_estudiante or 'nombre' not in new_estudiante or 'correo' not in new_estudiante or 'carrera' not in new_estudiante:
        return jsonify({'error': 'Datos incompletos del estudiante'}), 400
    
    # Verificar si el estudiante ya existe en la base de datos
    query = "SELECT * FROM estudiantes WHERE cedula = %s"
    existing_student = fetch_one(query, (new_estudiante['cedula'],))
    if existing_student:
        return jsonify({'error': 'El estudiante ya existe en la base de datos'}), 409  # 409 Conflict
    
    # Si el estudiante no existe, procede con la inserción
    insert_query = '''
    INSERT INTO estudiantes (cedula, nombre, correo, carrera)
    VALUES (%s, %s, %s, %s)
    '''
    params = (new_estudiante['cedula'], new_estudiante['nombre'], new_estudiante['correo'], new_estudiante['carrera'])
    execute_query(insert_query, params)

    return jsonify({'message': 'Estudiante añadido exitosamente'}), 201

#GET (todos)

@routes.route('/estudiantesTodos', methods=['GET'])
def get_estudiantes():
    query = "SELECT * FROM estudiantes"
    estudiantes = fetch_all(query)
    return jsonify(estudiantes)

#GET (por cédula)

@routes.route('/estudiantes/<cedula>', methods=['GET'])
def get_estudiante(cedula):
    query = "SELECT * FROM estudiantes WHERE cedula = %s"
    estudiante = fetch_one(query, (cedula,))
    if estudiante:
        return jsonify(estudiante)
    return jsonify({'message': 'Estudiante no encontrado'}), 404

#PUT (actualizar)
@routes.route('/estudiantes/<cedula>', methods=['PUT'])
def update_estudiante(cedula):
    update_data = request.json
    query = '''
    UPDATE estudiantes
    SET nombre = %s, correo = %s, carrera = %s
    WHERE cedula = %s
    '''
    params = (update_data['nombre'], update_data['correo'], update_data['carrera'], cedula)
    execute_query(query, params)
    return jsonify({'message': 'Estudiante actualizado exitosamente'})

#DELETE

@routes.route('/estudiantes/<cedula>', methods=['DELETE'])
def delete_estudiante(cedula):
    query = "DELETE FROM estudiantes WHERE cedula = %s"
    execute_query(query, (cedula,))
    return jsonify({'message': 'Estudiante eliminado exitosamente'})