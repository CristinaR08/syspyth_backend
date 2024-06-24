from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_one, fetch_all
from datetime import datetime, timedelta

registro_estudiantes_routes = Blueprint('registro_estudiantes_routes', __name__)

# POST
@registro_estudiantes_routes.route('/registrar', methods=['POST'])
def registrar_estudiante():
    data = request.get_json()
    cedula = data['cedula']
    numero_maquina = data['numero_maquina']
    sala = data['sala']
    fecha_hora = datetime.now()
    confirmado = False

# Consultar los demás datos del estudiante usando la cédula
    query_estudiante = "SELECT nombre, apellido, correo, carrera FROM estudiantes WHERE cedula = %s"
    estudiante = fetch_one(query_estudiante, (cedula,))
    
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    nombre_estudiante = estudiante['nombre']
    apellido_estudiante = estudiante['apellido']
    correo = estudiante['correo']
    carrera = estudiante['carrera']

    # Verificar si ya existe un registro con la misma cédula en los últimos 45 minutos
    query_check = '''
    SELECT * FROM registro_estudiantes 
    WHERE cedula = %s AND fecha_hora >= %s
    '''
    tiempo_limite = fecha_hora - timedelta(minutes=45)
    registro_reciente = fetch_one(query_check, (cedula, tiempo_limite))

    if registro_reciente:
        return jsonify({'error': 'Estudiante ya registrado, intente nuevamente en 45 minutos'}), 400


    # Insertar datos en la tabla registro_estudiantes
    query_insert = '''
    INSERT INTO registro_estudiantes (cedula, nombre, apellido, correo, carrera, numero_maquina, sala, fecha_hora, confirmacion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    execute_query(query_insert, (cedula, nombre_estudiante, apellido_estudiante, correo, carrera, numero_maquina, sala, fecha_hora, confirmado))

    return jsonify({'message': 'Estudiante registrado exitosamente'}), 201

@registro_estudiantes_routes.route('/no_confirmados', methods=['GET'])
def get_estudiantes_no_confirmados():
    query = "SELECT * FROM registro_estudiantes WHERE confirmado = FALSE"
    estudiantes_no_confirmados = fetch_all(query)
    return jsonify(estudiantes_no_confirmados)

#GET(fecha)
@registro_estudiantes_routes.route('/fecha', methods=['GET']) #/fecha?fecha=2024-06-07
def get_fecha_registro():
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'error':'Falta el parámetro fecha'}), 400

    query = "SELECT * FROM registro_estudiantes WHERE DATE(fecha_hora)=%s"
    registros = fetch_all(query,(fecha,))
    if not registros:
        return jsonify({'error':'No se encontraron registros para la fecha seleccionada'}), 404 
    return jsonify(registros)

#GET(numero_maquina)
@registro_estudiantes_routes.route('/numero_maquina/<numero_maquina>', methods=['GET'])
def get_maquina(numero_maquina):
    query = "SELECT * FROM registro_estudiantes WHERE numero_maquina = %s"
    registros = fetch_all(query,(numero_maquina,))
    if not registros:
        return jsonify({'message' : '"No se encontraron registros con ese número de máquina'}),404
    return jsonify(registros)

# UPDATE quizá se elimine
@registro_estudiantes_routes.route('/actualizar/<int:id>', methods=['PUT'])
def update_registro_estudiante(id):
    data = request.json

    # Verificar si el registro de estudiante existe
    query = "SELECT * FROM registro_estudiantes WHERE id = %s"
    registro = fetch_one(query, (id,))
    if not registro:
        return jsonify({'error': 'Registro de estudiante no encontrado'}), 404
    
    # Actualizar el registro de estudiante
    update_query = '''
    UPDATE registro_estudiantes
    SET numero_maquina = %s, materia = %s
    WHERE id = %s
    '''
    params = (data['numero_maquina'], data['materia'], id)
    execute_query(update_query, params)

    return jsonify({'message': 'Registro de estudiante actualizado exitosamente'})

# DELETE 
@registro_estudiantes_routes.route('/eliminar/<int:id>', methods=['DELETE'])
def delete_registro_estudiante(id):
    
    #Verificar si el registro de estudiante existe
    query = "SELECT * FROM registro_estudiantes WHERE id = %s"
    registro = fetch_one(query, (id,))
    if not registro:
        return jsonify({'error': 'Registro de estudiante no encontrado'}), 404
    
    #Eliminar el registro de estudiante
    delete_query = "DELETE FROM registro_estudiantes WHERE id = %s"
    execute_query(delete_query, (id,))

    # Actualizar los ids restantes para que no haya saltos
    update_query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT id FROM registro_estudiantes WHERE id > %s ORDER BY id) LOOP
            EXECUTE 'UPDATE registro_estudiantes SET id = ' || (r.id - 1) || ' WHERE id = ' || r.id;
        END LOOP;
    END $$;
    """
    execute_query(update_query, (id,))
    
    #Reiniciar la secuencia del id
    reset_sequence_query = "SELECT setval('registro_estudiantes_id_seq', COALESCE(MAX(id), 1)) FROM registro_estudiantes"
    execute_query(reset_sequence_query)
    
    return jsonify({'message': 'Registro de estudiante eliminado exitosamente'})