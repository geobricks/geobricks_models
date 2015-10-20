import rasterio
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename
from geobricks_models.utils.utils_rasterio import initialize_rasterio_raster

log = logger(__file__)

# TODO: multiply ndvi anomaly with wheat

def multiply_raster(input_raster1, input_raster2, output_path=None):

    # indicator, cultivation

    output_layer_path = create_tmp_filename('geotiff', 'multiply_raster_')

    r1 = rasterio.open(input_raster1)
    r_data1 = r1.read_band(1).astype(float).flatten()

    r2 = rasterio.open(input_raster2)
    r_data2 = r2.read_band(1).astype(float).flatten()

    nodata1 = r1.meta['nodata'] if 'nodata' in r1.meta else None
    nodata2 = r2.meta['nodata'] if 'nodata' in r2.meta else None

    index1 = (r_data1 != nodata1)
    index2 = (r_data2 != nodata2)

    r_data1 = index1 * r_data1
    r_data2 = index2 * r_data2

    # initialize output raster
    data, kwargs = initialize_rasterio_raster(r1, rasterio.float32)

    data = (r_data1 * r_data2)

    with rasterio.open(output_layer_path, 'w', **kwargs) as dst:
        dst.write_band(1, data.reshape(r1.shape[0], r1.shape[1]).astype(rasterio.float32))

    return output_layer_path


def multiply_raster_excluding_nodata(input_raster1, input_raster2, output_path=None):

    output_layer_path = create_tmp_filename('geotiff', 'multiply_raster_')

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