import rasterio
import numpy as np
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename

from geobricks_models.utils.utils_rasterio import initialize_rasterio_raster

log = logger(__file__)


# cut the raster layer by a max_threshold i.e. < -30%
def mask_raster_by_thresholds(input_raster, min=None, max=None, nodata=None):

    print min, max, nodata

    output_layer_path = create_tmp_filename('geotiff', 'indicator_mask_')

    r = rasterio.open(input_raster)
    r_data = r.read_band(1).astype(float).flatten()

    # initialize output raster TODO: avoid data that is not used
    data, kwargs = initialize_rasterio_raster(r, rasterio.float32)

    # get nodata value and min and min max values
    nodata_computed = r.meta['nodata'] if 'nodata' in r.meta else None
    min_computed = np.nanmin(r_data)
    max_computed = np.nanmax(r_data)

    # ge the right thresholds
    if min is None:
        min = min_computed

    if max is None:
        max = max_computed

    if nodata is None:
        nodata = nodata_computed

    # compute treshold
    data = _compute_thresholds(r_data, min, max, nodata)

    print min, max, nodata
    print data

    # Writing output file
    log.info("Mask_raster_by_thresholds: " + output_layer_path)
    with rasterio.open(output_layer_path, 'w', **kwargs) as dst:
        dst.write_band(1, data.reshape(r.shape[0], r.shape[1]).astype(rasterio.float32))

    return output_layer_path

def _compute_thresholds(array, min, max, nodata=None):

    index = (array > min) & (array <= max) & (array != nodata)

    return index



# cut_by_threshold('/media/vortex/LaCie/nena/wheat_area1.tif', '/media/vortex/LaCie/nena', 0.15)