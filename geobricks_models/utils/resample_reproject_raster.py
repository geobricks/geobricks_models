import os
import subprocess
from geobricks_common.core.log import logger
from geobricks_common.core.log import logger

log = logger(__file__)

# TODO: resample and reproject raster with gdalwarp
# gdalwarp apple_area1.tif apple_area1_res.tif -overwrite -co COMPRESS=DEFLATE -tr 0.083333340000000 -0.08333334000000 -r cubic


def resample(input_file, output_file=None, pixel_size='0.08333334', resample_algorithm='cubic'):
    log.info(pixel_size)

    output_file = "/media/vortex/LaCie/nena/resample.tif"

    # crop the layer on cutline
    args = [
        "gdalwarp",
        "-q",
        "-overwrite",
        "-multi",
        "-of", "GTiff",
        "-co", "COMPRESS=DEFLATE",
        # "-tr", float(pixel_size) float(pixel_size),
        "-tr", str(pixel_size) + " " + str(pixel_size),
        "-r", resample_algorithm,
        input_file,
        output_file
    ]
    try:
        log.info(args)
        test = ' '.join(str(x) for x in args)
        print test
        #TODO: handle subprocess Error (like that is not taken)
        output = subprocess.check_output(args)
        # stdout_value, error = proc.communicate()
        log.info(output)
    except Exception, e:
        print e


resample('/media/vortex/LaCie/nena/ndvi_cut.geotiff')