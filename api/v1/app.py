#!/usr/bin/python3
"""
Flask application integrating with an AirBnB static HTML template.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Universal Flask application variable: `app`
app = Flask(__name__)
swagger = Swagger(app)

# Flask server environment configuration
app.url_map.strict_slashes = False

# Configuration of the Flask server environment
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing (CORS)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# The `app_views` Blueprint established in `api.v1.views`
app.register_blueprint(app_views)


# Initiate Flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    Following each request, this method calls `.close()`
    (i.e., `.remove()`) on the current SQLAlchemy Session.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Manages 404 errors in case the global error handler fails.
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """
    Manages 404 errors in case the global error handler fails.
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Universal route to handle all error status codes.
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This modifies the `HTTPException` class with a custom error function.
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    Primary Flask application
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
