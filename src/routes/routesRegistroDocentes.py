#probablemente se elimine esta clase
from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all,fetch_one
from datetime import datetime

registro_docentes_routes = Blueprint('registro_docentes_routes', __name__)

# POST
@registro_docentes_routes.route('/confirmar', methods=['POST'])
def confirmar_registro():
    data = request.get_json()
    cedula_docente = data['cedula_docente']
    nombre_docente = data['nombre_docente']
    apellido_docente = data['apellido_docente']
    correo_docente = data['correo_docente']
    paralelo = data['paralelo']
    semestre = data['semestre']
    sala = data['sala']
    estudiante_ids = data['estudiante_ids']  # Lista de IDs de estudiantes a confirmar

    for estudiante_id in estudiante_ids:
        # Actualizar el registro del estudiante para marcarlo como confirmado
        update_estudiante_query = "UPDATE registro_estudiantes SET confirmado = TRUE WHERE id = %s"
        execute_query(update_estudiante_query, (estudiante_id,))

        # Obtener los datos del estudiante
        query_estudiante = "SELECT * FROM registro_estudiantes WHERE id = %s"
        estudiante = fetch_one(query_estudiante, (estudiante_id,))

        # Insertar en la tabla de asistencias
        query_asistencia = '''
        INSERT INTO asistencias (cedula_estudiante, nombre_estudiante, apellido_estudiante, correo_estudiante, carrera_estudiante,
                                 numero_maquina_estudiante, cedula_docente, nombre_docente, apellido_docente, correo_docente,
                                 materia, semestre, paralelo, aula, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        execute_query(query_asistencia, (estudiante['cedula'], estudiante['nombre_estudiante'], estudiante['apellido_estudiante'],
                                         estudiante['correo'], estudiante['carrera'], estudiante['numero_maquina'],
                                         cedula_docente, nombre_docente, apellido_docente, correo_docente,
                                         estudiante['materia'], semestre, paralelo, sala, datetime.now()))

    return jsonify({'message': 'Registros confirmados y asistencia actualizada'}), 201

# GET(todos)
@registro_docentes_routes.route('/lista', methods=['GET'])
def get_registro_docentes():
    query = "SELECT * FROM registro_docentes"
    registros = fetch_all(query)
    return jsonify(registros)

#GET(fecha)
@registro_docentes_routes.route('/fecha', methods=['GET']) #/fecha?fecha=2024-06-07
def get_fecha_registro():
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'error':'Falta el parámetro fecha'}), 400

    query = "SELECT * FROM registro_docentes WHERE DATE(fecha_hora)=%s"
    registros = fetch_all(query,(fecha,))
    if not registros:
        return jsonify({'error':'No se encontraron registros del docente para la fecha seleccionada'}), 404 
    return jsonify(registros)

#GET(sala)
@registro_docentes_routes.route('/sala/<sala>', methods=['GET'])
def get_sala(sala):
    query = "SELECT * FROM registro_docentes WHERE sala = %s"
    registros = fetch_all(query,(sala,))
    if not registros:
        return jsonify({'message' : '"No se encontraron registros con esa sala'}),404
    return jsonify(registros)

#GET(docente CI)
@registro_docentes_routes.route('/cedula/<cedula>', methods=['GET'])
def get_cedula(cedula):
    query = "SELECT * FROM registro_docentes WHERE cedula = %s"
    registros = fetch_all(query,(cedula,))
    if not registros:
        return jsonify({'message' : '"No se encontraron registros del docente con esa cedula'}),404
    return jsonify(registros)

# UPDATE quizá se elimine
@registro_docentes_routes.route('/actualizar/<int:id>', methods=['PUT'])
def update_registro_docente(id):
    data = request.json

    # Verificar si el registro de docente existe
    query = "SELECT * FROM registro_docentes WHERE id = %s"
    registro = fetch_one(query, (id,))
    if not registro:
        return jsonify({'error': 'Registro de docente no encontrado'}), 404
    
    # Actualizar el registro de docente
    update_query = '''
    UPDATE registro_docentes
    SET semestre = %s, paralelo = %s, sala = %s, materia = %s
    WHERE id = %s
    '''
    params = (data['semestre'], data['paralelo'], data['sala'], data['materia'], id)
    execute_query(update_query, params)

    return jsonify({'message': 'Registro del docente actualizado exitosamente'})

# DELETE 
@registro_docentes_routes.route('/eliminar/<int:id>', methods=['DELETE'])
def delete_registro_docente(id):
    
    query = "SELECT * FROM registro_docentes WHERE id = %s"
    registro = fetch_one(query, (id,))
    if not registro:
        return jsonify({'error': 'Registro de docente no encontrado'}), 404
    
    #Eliminar
    delete_query = "DELETE FROM registro_docentes WHERE id = %s"
    execute_query(delete_query, (id,))

    # Actualizar los ids
    update_query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT id FROM registro_docentes WHERE id > %s ORDER BY id) LOOP
            EXECUTE 'UPDATE registro_docentes SET id = ' || (r.id - 1) || ' WHERE id = ' || r.id;
        END LOOP;
    END $$;
    """
    execute_query(update_query, (id,))
    
    #Reiniciar la secuencia del id
    reset_sequence_query = "SELECT setval('registro_docentes_id_seq', COALESCE(MAX(id), 1)) FROM registro_docentes"
    execute_query(reset_sequence_query)
    
    return jsonify({'message': 'Registro del docente eliminado'})