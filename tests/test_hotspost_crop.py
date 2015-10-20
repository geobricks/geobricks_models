import unittest
from geobricks_models.core.hotspot_crop import calc_hotspot

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
        # 'layerName': 'gaul1_nena_4326',
        'layerName': 'afg_gaul1',

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
            'codes': [272, 273, 274, 275, 278, 282, 283, 289, 298, 299, 300],
            #  'codes': [278],
            # TODO: find a proper name instead of output (this should be the same as in geostatistics?)
            'output': ['adm1_name', 'adm1_code']
        },
        # TODO check other vector label
    },
    # TODO check the other stats
    'stats': {
        'zonalsum': {
            # weight of the zonalsum pixel
            # 'weight': 0.01
            'weight': 0.01
        }
    },

    # TODO: is it the right name?
    'model_options': {
        'threshold': {
            'min': None,
            # 'max': -30
            'max': -30
        },
        'resampling': 'near'
    }

}

class GeobricksTest(unittest.TestCase):

    # Raster
    def test_hotspot_crop(self):
        result = calc_hotspot(obj)
        print result



def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()




