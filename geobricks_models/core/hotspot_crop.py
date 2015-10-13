from geobricks_common.core.filesystem import get_raster_path
from geobricks_common.core.filesystem import get_vector_path
from geobricks_common.core.log import logger

log = logger(__file__)

def test():

    raster_path = get_raster_path({
        "datasource": ["geoserver"],
        'workspace': 'ndvi_anomaly',
        'layerName': 'ndvi_anomaly_1km_mod13a3_200803_3857'
    })

    vector_path = get_vector_path({
        "datasource": ["storage"],
        'layerName': 'gaul1_nena_4326'
    })

    print raster_path
    print vector_path



test()