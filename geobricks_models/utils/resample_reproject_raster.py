import os
import subprocess
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename

log = logger(__file__)

# TODO: resample and reproject raster with gdalwarp
# gdalwarp apple_area1.tif apple_area1_res.tif -overwrite -co COMPRESS=DEFLATE -tr 0.083333340000000 -0.08333334000000 -r cubic


def resample(input_file, pixel_size='0.08333334', s_srs=None, t_srs=None, resample_algorithm='cubic'):
    log.info(pixel_size)

    output_file = warp(input_file, s_srs, t_srs)
    print output_file
    output_file = pixel_resize(output_file, pixel_size, resample_algorithm)
    print output_file

    return output_file


def warp(input_file, s_srs=None, t_srs=None,):
    # -q -overwrite -multi -of GTiff -co COMPRESS=DEFLATE -s_srs 'EPSG:3857' -t_srs 'EPSG:4326' /media/vortex/LaCie/nena/geobricks_filesystem/tmp/indicator_mask_9545ad7d-ef78-4ef6-a5ca-bc8f8c41b676.geotiff /media/vortex/LaCie/nena/geobricks_filesystem/tmp/resample_70b85694-ac7a-41d0-819a-f631c1875290.geotiff
    print "warp"

    output_file = create_tmp_filename('geotiff', 'warp_')

    # warp
    args = [
        "gdalwarp",
        "-q",
        "-overwrite",
        "-multi",
        "-of", "GTiff",
        "-co", "COMPRESS=DEFLATE",
        "-s_srs", s_srs,
        "-t_srs", t_srs,
        input_file,
        output_file
    ]
    try:
        log.info(args)
        log.info(' '.join(str(x) for x in args))
        #TODO: handle subprocess Error (like that is not taken)
        output = subprocess.check_output(args)
        return output_file
    except Exception, e:
        print e

def pixel_resize(input_file, pixel_size='0.08333334', resample_algorithm='cubic'):

    output_file = create_tmp_filename('geotiff', 'resample_')

    # pixel_resize
    args = [
        "gdalwarp",
        "-q",
        "-overwrite",
        "-multi",
        "-of", "GTiff",
        "-co", "COMPRESS=DEFLATE",
        "-tr",
        pixel_size,
        pixel_size,
        "-r", resample_algorithm,
        input_file,
        output_file
    ]
    try:
        log.info(args)
        log.info(' '.join(str(x) for x in args))
        #TODO: handle subprocess Error (like that is not taken)
        output = subprocess.check_output(args)
        return output_file
    except Exception, e:
        print e

