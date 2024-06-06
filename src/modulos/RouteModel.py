from database.db import get_connection
from .entities.Route import Route

class RouteModel():

    @classmethod
    def get_routes(self):
        try:
            connection = get_connection()
            routes = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, duration, released FROM route ORDER BY title ASC")
                resultset = cursor.fetchall()

                for fila in resultset:
                    route = Route(fila[0], fila[1], fila[2], fila[3])
                    routes.append(route.to_JSON())
            connection.close()
            return routes
        except Exception as e:
            raise Exception(e)