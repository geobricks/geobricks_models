from geobricks_common.core.filesystem import get_raster_path
from geobricks_common.core.filesystem import get_vector_path
from geobricks_common.core.log import logger

from geobricks_models.utils.filter_shapefile import cut_shp
from geobricks_models.utils import crop_raster
from geobricks_models.utils.mask_threshold import mask_raster_by_thresholds
from geobricks_gis_raster.core.raster import get_srid, get_pixel_size
import rasterio

log = logger(__file__)


def calc_hotspot(obj):
    print obj

    # mapping objects
    vector = obj['vector']
    raster = obj['raster']
    model_options = obj['model_options']
    zonalsum_options = obj['stats']['zonalsum']

    # create new AOI shapefile
    shp_path = get_vector_path(vector)
    aoi_shp_path = cut_shp(shp_path, vector['filter'])

    # extract bbox AOI indicator (i.e. NDVI)
    indicator_path = get_raster_path(raster[0])
    indicator_aoi_path = crop_raster.crop_by_shapefile_bbox(indicator_path, aoi_shp_path)

    # extract bbox AOI cultivation/crop (i.e. WHEAT)
    cultivation_path = get_raster_path(raster[1])
    cultivation_aoi_path = crop_raster.crop_by_shapefile_bbox(cultivation_path, aoi_shp_path)

    # indicator_mask AOI indicator with threshold
    min = model_options['threshold']['min'] if 'min' in model_options['threshold'] else None
    max = model_options['threshold']['max'] if 'max' in model_options['threshold'] else None
    indicator_aoi_mask_path = mask_raster_by_thresholds(indicator_aoi_path, min, max)

    # reproject indicator to cultivation crs
    with rasterio.open(cultivation_aoi_path) as source:
        print source.meta

    source_crs = 'EPSG:' + get_srid(cultivation_aoi_path)
    source_pixel_size = get_pixel_size(cultivation_aoi_path)
    print source_pixel_size


    # resample indicator to cultivation pixel size
    # TODO: how to do snapping (affine?) both pixels
    # TODO: check if they are of the same size

    # hotspot_aoi_layer = multiply ndvi_mask * wheat

    # for each gaul1 cut the hotspot_aoi_layer

    # calc for each gaul1 the zonalsum





obj = {
    'raster': [
        {
            'datasource': ['geoserver'],
            'workspace': 'ndvi_anomaly',
            'layerName': 'ndvi_anomaly_1km_mod13a3_200803_3857'
        },
        {
            'datasource': ['storage'],
            'layerName': 'wheat_area_4326'
        }
    ],
    # TODO check the other vector definition
    'vector': {
        'datasource': 'storage',
        'type': 'shapefile',
        'layerName': 'gaul1_nena_4326',

        # TODO: geostatistics example
        # 'options': {
        #     'layer': 'gaul1_2015_4326',  # required (table or table alias)
        #     'column': 'adm0_name',  # required (column or column_alias)
        #     'codes': ['Italy'],
        #     'groupby': ['adm1_code', 'adm1_name']  # optional used to get subcodes (i.e. get all italian's region)
        # },

        #  TODO: check the other vector filter definition (this should be the same as in geostatistics?)
        'filter': {
            'column': 'adm1_code',
            'codes': [61525, 2755],
            # TODO: find a proper name instead of output (this should be the same as in geostatistics?)
            'output': ['adm1_name', 'adm1_code']
        },
        # TODO check other vector label
    },
    # TODO check the other stats
    'stats': {
        'zonalsum': {
            # weight of the zonalsum pixel
            'weight': 10
        }
    },

    # TODO: is it the right name?
    'model_options': {
        'threshold': {
            'min': None,
            'max': -30
        }
    },

}

calc_hotspot(obj)