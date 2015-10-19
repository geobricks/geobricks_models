import json
from flask import Blueprint
from flask import Response, request
from flask.ext.cors import cross_origin
from geobricks_models.core.hotspot_crop import calc_hotspot

app = Blueprint("geobricks_models", "geobricks_models")


@app.route('/', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def root():
    """
    Root REST service.
    @return: Welcome message.
    """
    return 'Welcome to Geobricks Common!'

@app.route('/discovery/', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'common',
        'title': 'Geobricks Models Service',
        'description': 'Functionalities to handle Models.',
        'type': 'SERVICE',

    }
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/hotspot/crops/', methods=['POST'])
@app.route('/hotspot/crops', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_scatter_plot():
    try:
        user_json = request.get_json()
        result = calc_hotspot(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e.get_message(), e.get_status_code())