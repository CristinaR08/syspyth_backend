from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all, fetch_one

routes_estudiantes = Blueprint('routes_estudiante', __name__)

#POST
@routes_estudiantes.route('/registrar', methods=['POST'])
def add_estudiante():
    new_estudiante = request.json

    print("Datos del estudiante recibidos:", new_estudiante)

    # Validar que los datos del estudiante están presentes
    if not new_estudiante or 'cedula' not in new_estudiante or 'nombre' not in new_estudiante or 'apellido'  not in new_estudiante or 'correo' not in new_estudiante or 'carrera' not in new_estudiante:
        return jsonify({'error': 'Datos incompletos del estudiante'}), 400
    
    # Verificar si el estudiante ya existe en la base de datos por cédula o correo electrónico
    query_by_cedula = "SELECT * FROM estudiantes WHERE cedula = %s"
    existing_student_by_cedula = fetch_one(query_by_cedula, (new_estudiante['cedula'],))
    query_by_correo = "SELECT * FROM estudiantes WHERE correo = %s"
    existing_student_by_correo = fetch_one(query_by_correo, (new_estudiante['correo'],))
    
    if existing_student_by_cedula:
        return jsonify({'error': 'La cédula ya está registrada para otro estudiante'}), 409  # 409 Conflict
    
    if existing_student_by_correo:
        return jsonify({'error': 'El correo electrónico ya está registrado para otro estudiante'}), 409  # 409 Conflict
    
    #Validar la terminación del correo electrónico
    if not new_estudiante['correo'].endswith('@uce.edu.ec'):
        return jsonify({'error': 'El correo electrónico debe ser de la UCE'}), 400
    

    # Si el estudiante no existe, procede con la inserción
    insert_query = '''
    INSERT INTO estudiantes (cedula, nombre, apellido, correo, carrera)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    '''
    params = (new_estudiante['cedula'], new_estudiante['nombre'], new_estudiante['apellido'], new_estudiante['correo'], new_estudiante['carrera'])
    estudiante_id = execute_query(insert_query, params, fetch_result=True)

    return jsonify({'message': 'Estudiante añadido exitosamente', 'id': estudiante_id}), 201

#GET (todos)

@routes_estudiantes.route('/lista', methods=['GET'])
def get_estudiantes():
    query = "SELECT * FROM estudiantes"
    estudiantes = fetch_all(query)
    return jsonify(estudiantes)

#GET (por cédula)

@routes_estudiantes.route('/consultar/<cedula>', methods=['GET'])
def get_estudiante(cedula):
    query = "SELECT * FROM estudiantes WHERE cedula = %s"
    estudiante = fetch_one(query, (cedula,))
    if estudiante:
        return jsonify(estudiante)
    return jsonify({'message': 'Estudiante no encontrado'}), 404

#PUT (actualizar)
@routes_estudiantes.route('/actualizar/<cedula>', methods=['PUT'])
def update_estudiante(cedula):
    update_data = request.json
    query = '''
    UPDATE estudiantes
    SET nombre = %s, apellido = %s, correo = %s, carrera = %s
    WHERE cedula = %s
    '''
    params = (update_data['nombre'], update_data['apellido'] ,update_data['correo'], update_data['carrera'], cedula)
    execute_query(query, params)
    return jsonify({'message': 'Estudiante actualizado exitosamente'})

#DELETE

@routes_estudiantes.route('/eliminar/<cedula>', methods=['DELETE'])
def delete_estudiante(cedula):
    # Verificar si el estudiante existe
    query = "SELECT id FROM estudiantes WHERE cedula = %s"
    estudiante = fetch_one(query, (cedula,))
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    # Obtener el ID del estudiante
    estudiante_id = estudiante['id']
    
    # Eliminar el estudiante
    delete_query = "DELETE FROM estudiantes WHERE cedula = %s"
    execute_query(delete_query, (cedula,))
    
    # Actualizar los IDs restantes
    update_query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT id FROM estudiantes WHERE id > %s ORDER BY id) LOOP
            EXECUTE 'UPDATE estudiantes SET id = ' || (r.id - 1) || ' WHERE id = ' || r.id;
        END LOOP;
    END $$;
    """
    execute_query(update_query, (estudiante_id,))
    
    # Reiniciar la secuencia del ID
    reset_sequence_query = "SELECT setval('estudiantes_id_seq', COALESCE(MAX(id), 1)) FROM estudiantes"
    execute_query(reset_sequence_query)
    
    return jsonify({'message': 'Estudiante eliminado exitosamente'})