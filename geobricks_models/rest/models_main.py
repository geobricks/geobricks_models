from flask import Flask
from flask.ext.cors import CORS
from geobricks_models.config.config import config
from geobricks_models.rest import models_rest as rest
import logging

# Initialize the Flask app
app = Flask(__name__)

# Initialize CORS filters
cors = CORS(app, resources={r'/*': {'origins': '*'}})

# Core services.
app.register_blueprint(rest.app, url_prefix='/models')

# Logging level.
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Start Flask server
if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=config['debug'], threaded=True)