from database.db import execute_query

def create_tables():
    # Tabla estudiantes
    estudiantes_query = '''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id SERIAL PRIMARY KEY,
        cedula VARCHAR(10) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NOT NULL,
        carrera VARCHAR(100) NOT NULL
    )
    '''
    execute_query(estudiantes_query)

    # Tabla docentes
    docentes_query = '''
    CREATE TABLE IF NOT EXISTS docentes (
        id SERIAL PRIMARY KEY,
        cedula VARCHAR(10) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NOT NULL,
        contraseña VARCHAR(100) NOT NULL
    )
    '''
    execute_query(docentes_query)

    #Tabla administradores
    administradores_query =  '''
    CREATE TABLE IF NOT EXISTS administradores (
        id SERIAL PRIMARY KEY,
        cedula VARCHAR(10) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NOT NULL,
        username VARCHAR(20) UNIQUE NOT NULL,
        contraseña VARCHAR(255) NOT NULL
    );
    '''
    execute_query(administradores_query)

    #Tabla registrto estudiantes
    registro_estudiantes_query =  '''
    CREATE TABLE IF NOT EXISTS registro_estudiantes(
        id SERIAL PRIMARY KEY,
        cedula VARCHAR(10) NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NOT NULL,
        carrera VARCHAR(100), 
        numero_maquina VARCHAR(20) NOT NULL,
        sala VARCHAR(10) NOT NULL,
        fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        confirmacion BOOLEAN DEFAULT FALSE
    );
    '''
    execute_query(registro_estudiantes_query)

    #  Tabla asistencia
    asistencia_query = '''
    CREATE TABLE IF NOT EXISTS asistencias (
        id SERIAL PRIMARY KEY,
        cedula_docente VARCHAR(10) UNIQUE NOT NULL,
        nombre_docente VARCHAR(100) NOT NULL,
        apellido_docente VARCHAR(100) NOT NULL,
        correo_docente VARCHAR(100) NOT NULL,
        cedula_estudiante VARCHAR(10) UNIQUE NOT NULL,
        nombre_estudiante VARCHAR(100) NOT NULL,
        apellido_estudiante VARCHAR(100) NOT NULL,
        correo_estudiante VARCHAR(100) NOT NULL,
        carrera_estudiante VARCHAR(100) NOT NULL,
        numero_maquina_estudiante VARCHAR(10) NOT NULL,
        materia VARCHAR(100) NOT NULL,
        semestre VARCHAR(100) NOT NULL,
        paralelo VARCHAR(100) NOT NULL,
        aula VARCHAR(100) NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula),
        FOREIGN KEY (cedula_docente) REFERENCES docentes(cedula)
    )
    '''
    execute_query(asistencia_query)