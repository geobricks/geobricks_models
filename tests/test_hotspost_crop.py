import unittest
import os
from geobricks_common.core.filesystem import get_raster_path, get_raster_path_published, get_raster_path_storage, get_vector_path_storage, get_vector_path


class GeobricksTest(unittest.TestCase):

    # Raster
    def test_hotspot_crop(self):
        print



def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()


