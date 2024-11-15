from flask import Flask
from routes.home import home_route
from routes.cliente import cliente_route
from configuration import configure_all

app = Flask(__name__)

configure_all(app)

# app.register_blueprint(home_route)
# app.register_blueprint(cliente_route, url_prefix='/clientes')

app.run(debug=True)