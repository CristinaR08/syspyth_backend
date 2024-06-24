from flask import Blueprint, request, jsonify
from database.db import execute_query, fetch_all, fetch_one

routes_administrador = Blueprint('routes_administradores', __name__)

# POST
@routes_administrador.route('/registrar', methods=['POST'])
def add_administrador():
    new_admin = request.json

    # Validar que los datos del administrador están presentes
    if not new_admin or 'cedula' not in new_admin or 'nombre' not in new_admin or 'apellido' not in new_admin or 'correo' not in new_admin or 'username' not in new_admin or 'contraseña' not in new_admin :
        return jsonify({'error': 'Datos incompletos del administrador'}), 400
    
    # Verificar si el administrador ya existe en la base de datos por cédula, correo o username
    query_by_cedula = "SELECT * FROM administradores WHERE cedula = %s"
    existing_admin_by_cedula = fetch_one(query_by_cedula, (new_admin['cedula'],))
    
    query_by_correo = "SELECT * FROM administradores WHERE correo = %s"
    existing_admin_by_correo = fetch_one(query_by_correo, (new_admin['correo'],))
    
    query_by_username = "SELECT * FROM administradores WHERE username = %s"
    existing_admin_by_username = fetch_one(query_by_username, (new_admin['username'],))
    
    if existing_admin_by_cedula:
        return jsonify({'error': 'La cédula ya está registrada para otro administrador'}), 409  # 409 Conflict
    
    if existing_admin_by_correo:
        return jsonify({'error': 'El correo electrónico ya está registrado para otro administrador'}), 409  # 409 Conflict
    
    if existing_admin_by_username:
        return jsonify({'error': 'El username ya está registrado para otro administrador'}), 409  # 409 Conflict
    
    
    # Validar la terminación del correo electrónico
    if not new_admin['correo'].endswith('@uce.edu.ec'):
        return jsonify({'error': 'El correo electrónico debe ser de la UCE'}), 400
    
    # Si el admin no existe, se inserta
    insert_query = '''
    INSERT INTO administradores (cedula, nombre, apellido, correo, username, contraseña)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
    '''
    params = [new_admin['cedula'], new_admin['nombre'], new_admin['apellido'], new_admin['correo'],  new_admin['username'], new_admin['contraseña']]
    admin_id = execute_query(insert_query, params, fetch_result=True)

    # Devolver una respuesta
    return jsonify({'message': 'Administrador añadido exitosamente', 'id': admin_id}), 201


# GET
@routes_administrador.route('/lista', methods=['GET'])
def get_administradores():
    query = "SELECT * FROM administradores"
    registros = fetch_all(query)
    return jsonify(registros)

#GET (por cédula)
@routes_administrador.route('/consultar/<cedula>', methods=['GET'])
def get_administrador(cedula):
    query = "SELECT * FROM administradores WHERE cedula = %s"
    admin = fetch_one(query, (cedula,))
    if admin:
        return jsonify(admin)
    return jsonify({'message': 'Administrador no existente'}), 404

# UPDATE
@routes_administrador.route('/actualizar/<cedula>', methods=['PUT'])
def update_administrador(cedula):
    
    data = request.json

    # Verificar si el administrador existe
    query = "SELECT * FROM administradores WHERE cedula = %s"
    registro = fetch_one(query, (cedula,))
    if not registro:
        return jsonify({'error': 'Administrador no encontrado'}), 404
    
    # Actualizar el administrador
    update_query = '''
    UPDATE administradores
    SET nombre = %s, apellido = %, correo = %s, username = %s, contraseña = %s
    WHERE cedula = %s
    '''
    params = (data['nombre'], data['apellido'], data['correo'], data['username'], data['contraseña'])
    execute_query(update_query, params)

    return jsonify({'message': 'Administrador actualizado exitosamente'})

#DELETE
@routes_administrador.route('/eliminar/<cedula>', methods=['DELETE'])
def delete_admin(cedula):
     # Verificar si el docente existe
    query = "SELECT * FROM administradores WHERE cedula = %s"
    administradores = fetch_one(query, (cedula,))
    if not administradores:
        return jsonify({'error': 'Admin no encontrado'}), 404
    
    # Eliminar el docente
    delete_query = "DELETE FROM administradores WHERE cedula = %s"
    execute_query(delete_query, (cedula,))

    # Actualizar los IDs
    update_query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT id FROM administradores WHERE id > %s ORDER BY id) LOOP
            EXECUTE 'UPDATE administradores SET id = ' || (r.id - 1) || ' WHERE id = ' || r.id;
        END LOOP;
    END $$;
    """
    execute_query(update_query, (administradores['id'],))
    
    # Reiniciar la secuencia del ID
    reset_sequence_query = "SELECT setval('administradores_id_seq', COALESCE(MAX(id), 1)) FROM administradores"
    execute_query(reset_sequence_query)
    
    return jsonify({'message': 'administrador eliminado exitosamente'})
