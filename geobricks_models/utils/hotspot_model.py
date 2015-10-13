from filter_shapefile import cut_shp

# TODO: Model for hotspot analysis


def calc_hotspot(obj):
    print obj

    # create new AOI shapefile

    # extract bbox AOI NDVI

    # extract bbox AOI wheat

    # ndvi_mask AOI ndvi with threshold

    # reproject ndvi to wheat

    # resample ndvi to wheat

    # hotspot_aoi_layer = multiply ndvi_mask * wheat

    # for each gaul1 cut the hotspot_aoi_layer

    # calc for each gaul1 the zonalsum




obj = {
    'rasters': [
        {
            'workspace': '',
            'layername': '',
            'datasource': 'geoserver'
        },
        {
            'workspace': '',
            'layername': '',
            'datasource': 'geoserver'
        }
    ],
    # TODO check the other vector definition
    'vector': {
        'datasource': 'storage',
        'type': 'shapefile',
        'layername': 'gaul1',
        #  TODO: check the other vector filter definition
        'filters': {
            'property': "adm1_code",
            'codes': [61525, 2755],
        },
        # TODO check other vector label
        'output': ["adm1_name", "adm1_code"]
    },
    # TODO check the other stats
    'stats': {
        'zonalsum': {
            # weight of the zonalsum pixel
            'weight': 10
        }
    }

}




