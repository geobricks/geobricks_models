from copy import deepcopy
from geobricks_common.core.filesystem import get_raster_path
from geobricks_common.core.filesystem import get_vector_path
from geobricks_common.core.log import logger


# from geobricks_gis_raster.core.raster import get_srid, get_pixel_size
from geobricks_models.utils.utils_from_geobricks_gis_raster import get_srid, get_pixel_size, get_bbox

from geobricks_models.utils.filter_shapefile import cut_shp
from geobricks_models.utils import crop_raster
from geobricks_models.utils.mask_threshold import mask_raster_by_thresholds
from geobricks_models.utils.resample_reproject_raster import resample
from geobricks_models.utils.calc_aoi_hotspot import multiply_raster
from geobricks_models.utils.zonalsum import zonalsum


log = logger(__file__)


def calc_hotspot(obj):

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
    cultivation_aoi_srs = 'EPSG:' + get_srid(cultivation_aoi_path)
    cultivation_aoi_pixel_size = get_pixel_size(cultivation_aoi_path)
    west, south, east, north = get_bbox(cultivation_aoi_path)

    indicator_aoi_mask_srs = 'EPSG:' + get_srid(indicator_aoi_mask_path)

    # resample indicator to cultivation pixel size
    # TODO: how to do snapping (affine?) both pixels
    resampling = model_options.get('resampling', None)
    indicator_aoi_mask_resample_path = resample(indicator_aoi_mask_path,
                                                west, south, east, north,
                                                cultivation_aoi_pixel_size,
                                                indicator_aoi_mask_srs,
                                                cultivation_aoi_srs,
                                                resampling)

    # TODO: check if indicator and cultivation are of the same size
    # hotspot_aoi_layer = multiply ndvi_mask * wheat
    hotspot_aoi_layer_path = multiply_raster(indicator_aoi_mask_resample_path, cultivation_aoi_path)

    # for each gaul1 cut the hotspot_aoi_layer
    zonalsum_results = []
    for code in vector['filter']['codes']:

        filter = deepcopy(vector['filter'])
        filter['codes'] = [code]
        region_shp_path = cut_shp(shp_path, filter)

        # crop the hotspot_aoi_layer with region shp
        region_hotspot_path = crop_raster.by_shp(hotspot_aoi_layer_path, region_shp_path)

        # calc for each gaul1 the zonalsum
        value_area_affected = zonalsum(region_hotspot_path, zonalsum_options['weight'])

        cultivation_region_path = crop_raster.by_shp(cultivation_aoi_path, region_shp_path)
        value_cultivation_total = zonalsum(cultivation_region_path, zonalsum_options['weight'])

        zonalsum_results.append({
            'code': code,
            'c_aa': value_area_affected,
            'c_ac': value_cultivation_total,
            'perc': (value_area_affected / value_cultivation_total) * 100

        })

    for z in zonalsum_results:
        print z['code'], int(z['c_ac']), int(z['c_aa']), int(z['perc'])

    return zonalsum_results