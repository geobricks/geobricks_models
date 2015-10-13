import rasterio
import numpy as np
from geobricks_common.core.log import logger
from eco_countries_demo.processing.utils_rasterio import initialize_rasterio_raster

log = logger(__file__)


# cut the raster layer by a max_threshold i.e. < -30%
def cut_by_threshold(input_raster, output_path, max_threshold):

    output_layer_path = output_path + "/test.tif"

    r = rasterio.open(input_raster)
    r_data = r.read_band(1).astype(float).flatten()

    # initialize output raster TODO: avoid data that is not used
    data, kwargs = initialize_rasterio_raster(r, rasterio.float32)

    # get nodata value and min and min max values
    nodata = r.meta['nodata'] if 'nodata' in r.meta else None
    min_computed = np.nanmin(r_data)
    max_computed = np.nanmax(r_data)

    # compute treshold
    data = compute_thresholds(r_data, min_computed, max_threshold, nodata)

    # Writing output file
    output_layer_path = output_path + "/test.tif"
    print "Writing: ", output_layer_path
    with rasterio.open(output_layer_path, 'w', **kwargs) as dst:
        dst.write_band(1, data.reshape(r.shape[0], r.shape[1]).astype(rasterio.float32))


def compute_thresholds(array, min, max, nodata=None):

    index = (array > min) & (array <= max) & (array != nodata)

    return index



# cut_by_threshold('/media/vortex/LaCie/nena/wheat_area1.tif', '/media/vortex/LaCie/nena', 0.15)