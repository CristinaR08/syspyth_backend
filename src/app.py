from flask import Flask
from flask_cors import CORS
from config import config
from routes.routesEstudiante import routes_estudiates
from routes.routesDocente import routes_docentes
from routes.routesAdministrador import routes_administrador
from routes.routesRegistroEstudiantes import registro_estudiantes_routes
from routes.routesRegistroDocentes import registro_docentes_routes
from routes.routesAsistencia import routes_asistencia
from database.models import create_tables

app = Flask(__name__)
CORS(app)

# Configuración de la aplicación
app.config.from_object(config['development'])

# Crear tablas si no existen
with app.app_context():
    create_tables()

# Registrar rutas
app.register_blueprint(routes_estudiates, url_prefix='/api/v1.0/estudiantes')
app.register_blueprint(routes_docentes, url_prefix='/api/v1.0/docentes')
app.register_blueprint(routes_administrador, url_prefix='/api/v1.0/administrador')
app.register_blueprint(registro_estudiantes_routes, url_prefix='/api/v1.0/registro_estudiantes')
app.register_blueprint(registro_docentes_routes, url_prefix='/api/v1.0/registro_docentes')
app.register_blueprint(routes_asistencia, url_prefix='/api/v1.0/asistencia')


# Manejador de errores
def page_not_found(error):
    return "<h1>Not found page</h1>", 404

app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
