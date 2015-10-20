import rasterio
import subprocess
from geobricks_proj4_to_epsg.core.proj4_to_epsg import get_epsg_code_from_proj4
from geobricks_common.core.log import logger
import json

log = logger(__file__)


def get_authority(file_path):
    '''
    Get the authority used by a raster i.e. EPSG:4326
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    '''
    with rasterio.open(file_path) as src:
        log.info(src.meta)
        # if 'init' in src.meta['crs']:
        #     return src.meta['crs']['init']
        # elif 'proj' in src.meta['crs']:
        #     return src.meta['crs']['proj']
        if 'init' in src.meta['crs']:
            return src.meta['crs']['init']
        elif 'proj' in src.meta['crs']:
            # TODO: check if works (find a raster to test it...)
            return "EPSG:" + str(get_epsg_code_from_proj4(src.meta['crs']['proj']))
    return None

def get_srid(file_path):
    '''
    Get the SRID of a raster (i.e. 4326 or 3857 and not EPSG:4326)
    :param file_path: path to the file
    :return: return the SRID of the raster projection
    '''
    proj = get_authority(file_path)
    if ":" in proj:
        return proj.split(":")[1]
    if proj.isdigit():
        return proj
    return None


# TODO: make it nicer
def get_pixel_size(input_file, formula=None):
    # TODO: get pixel value with rasterio library?
    cmd = "gdalinfo " + input_file + " | grep Pixel"
    log.info(cmd)
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if "Pixel Size" in output:
            pixel_size = output[output.find("(")+1:output.find(",")]
            return str(pixel_size)
        return None
    except Exception, e:
        log.error(e)
        raise Exception(e, 400)


def get_bbox(input_file):

    try:
        process = subprocess.Popen(['rio', 'info', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        v = json.loads(output.strip().replace("'", "\""))
        west = v['bounds'][0]
        south = v['bounds'][1]
        east = v['bounds'][2]
        north = v['bounds'][3]
        return west, south, east, north
    except Exception, e:
        log.error(e)
        raise Exception(e, 400)