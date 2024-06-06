from flask import Flask
from config import config
from routes.routes import routes
app = Flask(__name__)

# Routes
app.register_blueprint(routes, url_prefix='/api/v1.0')

# Error handler
def page_not_found(error):
    return "<h1>Not found page</h1>", 404

app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
