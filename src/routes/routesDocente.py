from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all, fetch_one

routes_docentes = Blueprint('routes_docentes', __name__)

#POST
@routes_docentes.route('/registrar', methods=['POST'])
def add_docente():
    new_docente = request.json

    print("Datos del docente recibidos:", new_docente)

    # Validar datos
    if not new_docente or 'cedula' not in new_docente or 'nombre' not in new_docente or 'apellido'  not in new_docente or 'correo' not in new_docente or 'contraseña' not in new_docente:
        return jsonify({'error': 'Datos incompletos del docente'}), 400
    
    query_by_cedula = "SELECT * FROM docentes WHERE cedula = %s"
    existing_docente_by_cedula = fetch_one(query_by_cedula, (new_docente['cedula'],))
    query_by_correo = "SELECT * FROM docentes WHERE correo = %s"
    existing_docente_by_correo = fetch_one(query_by_correo, (new_docente['correo'],))
    
    if existing_docente_by_cedula:
        return jsonify({'error': 'La cédula ya está registrada para otro docente'}), 409  # 409 Conflict
    
    if existing_docente_by_correo:
        return jsonify({'error': 'El correo electrónico ya está registrado para otro docente'}), 409  # 409 Conflict
    
    
    #Validar la terminación del correo electrónico
    if not new_docente['correo'].endswith('@uce.edu.ec'):
        return jsonify({'error': 'El correo electrónico debe ser de la UCE'}), 400
    

    # Si no existe, crear
    insert_query = '''
    INSERT INTO docentes (cedula, nombre, apellido, correo, contraseña)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    '''
    params = (new_docente['cedula'], new_docente['nombre'], new_docente['apellido'], new_docente['correo'], new_docente['contraseña'])
    docente_id = execute_query(insert_query, params, fetch_result=True)

    return jsonify({'message': 'Docente añadido exitosamente', 'id': docente_id}), 201

#GET (todos)
@routes_docentes.route('/lista', methods=['GET'])
def get_docentes():
    query = "SELECT * FROM docentes"
    docentes = fetch_all(query)
    return jsonify(docentes)

#GET (por cédula)
@routes_docentes.route('/consultar/<cedula>', methods=['GET'])
def get_docente(cedula):
    query = "SELECT * FROM docentes WHERE cedula = %s"
    docente = fetch_one(query, (cedula,))
    if docente:
        return jsonify(docente)
    return jsonify({'message': 'Docente no encontrado'}), 404

#PUT(actualizar)
@routes_docentes.route('/actualizar/<cedula>', methods=['PUT'])
def update_docente(cedula):
    update_datos = request.json
    datos_requeridos = ['nombre', 'apellido', 'correo', 'contraseña']
    if not update_datos or any(dato not in update_datos for dato in datos_requeridos):
        return jsonify({'error':'Datos incompletos para la actualización'}), 400
    
    query = '''
    UPDATE docentes
    SET nombre = %s, apellido = %s, correo = %s, contraseña = %s
    WHERE cedula = %s    
    '''

    params = (update_datos['nombre'], update_datos['apellido'], update_datos['correo'], update_datos['contraseña'])
    execute_query(query, params)
    return jsonify({'message':'Docente actualizado exitosamente'})

#DELETE
@routes_docentes.route('/eliminar/<cedula>', methods=['DELETE'])
def delete_docente(cedula):
     # Verificar si el docente existe
    query = "SELECT * FROM docentes WHERE cedula = %s"
    docente = fetch_one(query, (cedula,))
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    
    # Eliminar el docente
    delete_query = "DELETE FROM docentes WHERE cedula = %s"
    execute_query(delete_query, (cedula,))

    # Actualizar los IDs
    update_query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT id FROM docentes WHERE id > %s ORDER BY id) LOOP
            EXECUTE 'UPDATE docentes SET id = ' || (r.id - 1) || ' WHERE id = ' || r.id;
        END LOOP;
    END $$;
    """
    execute_query(update_query, (docente['id'],))
    
    # Reiniciar la secuencia del ID
    reset_sequence_query = "SELECT setval('docentes_id_seq', COALESCE(MAX(id), 1)) FROM docentes"
    execute_query(reset_sequence_query)
    
    return jsonify({'message': 'Docente eliminado exitosamente'})

