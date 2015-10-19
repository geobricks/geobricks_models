import rasterio
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename
from geobricks_models.utils.utils_rasterio import initialize_rasterio_raster

log = logger(__file__)

# TODO: multiply ndvi anomaly with wheat

def multiply_raster(input_raster1, input_raster2, output_path=None):

    output_layer_path = create_tmp_filename('geotiff', 'multiply_raster_')

    print input_raster1
    print input_raster2

    r1 = rasterio.open(input_raster1)
    r_data1 = r1.read_band(1).astype(float)

    r2 = rasterio.open(input_raster2)
    r_data2 = r2.read_band(1).astype(float)

    # initialize output raster
    data, kwargs = initialize_rasterio_raster(r1, rasterio.float32)

    # calculate
    data = (r_data1 * r_data2)

    # Writing output file
    # TODO: random output filename
    log.info("Multiply Raster, Writing: " + output_layer_path)
    with rasterio.open(output_layer_path, 'w', **kwargs) as dst:
        dst.write_band(1, data.astype(rasterio.float32))

    return output_layer_path


# print multiply_raster('/media/vortex/LaCie/nena/wheat_area1.tif', '/media/vortex/LaCie/nena/test.tif', '/media/vortex/LaCie/nena/')