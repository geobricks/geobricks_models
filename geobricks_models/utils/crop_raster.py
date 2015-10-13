import fiona
import subprocess
from pyproj import Proj, transform
import rasterio
from geobricks_common.core.filesystem import create_tmp_filename
from geobricks_common.core.log import logger

log = logger(__file__)

# gdalwarp -cutline gaul1/GAUL0_NENA_level1.shp ndvi_anomaly/ndvi_anomaly_1km_mod13a3_200803_3857.geotiff ndvi_cut.geotiff
# gdalwarp -cutline gaul1/output/aio/shape.shp ndvi_cut.geotiff ndvi_subcut3.geotif

# -projwin west north east south
#fiona (minx, miny, maxx, maxy)	(west, south, east, north)

# TODO: check if raster and shp are of the same projection
def by_shp(input_raster, input_shp):

    log.info('Cropping: ' + input_raster + ' by ' + input_shp)

    output_file = crop_by_shapefile_bbox(input_raster, input_shp)

    return crop_by_shapefile_cutline(output_file, input_shp)


def crop_by_shapefile_bbox(input_raster, input_shp):

    log.info('Crop_by_shapefile_bbox: ' + input_raster + ' by ' + input_shp)

    with fiona.open(input_shp) as shp:

        # maxlat, minlat, maxlon, minlon = shp.bounds
        west, south, east, north = shp.bounds

        with rasterio.open(input_raster) as raster:

            # TODO: check both crs if exists
            p_in = Proj(shp.crs)
            p_out = Proj(raster.meta['crs'])

            # transform bbox to the right coordinate system
            west, south = transform(p_in, p_out, west, south)
            east, north = transform(p_in, p_out, east, north)

            # create tmp output file
            output_file = create_tmp_filename('geotiff', 'cut_by_bbox_')

            args = [
                'gdal_translate',
                '-projwin',
                str(west),
                str(north),
                str(east),
                str(south),
                input_raster,
                output_file
            ]

            try:
                # log.info(args)
                log.info(' '.join(args))
                #TODO: handle subprocess Error (like that is not taken)
                proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)

                return output_file

            except:
                stdout_value = proc.communicate()[0]
                raise Exception(stdout_value)


# cropping with the cutline
def crop_by_shapefile_cutline(input_raster, input_shp):

    log.info('Crop_by_shapefile_cutline: ' + input_raster + ' by ' + input_shp)

    output_file = create_tmp_filename('geotiff', 'cut_by_cutline_')

    args = [
        'gdalwarp', # gdalwarp -cutline gaul1/output/aio/shape.shp ndvi_cut.geotiff ndvi_subcut3.geotif',
        '-co', 'COMPRESS=DEFLATE'
        '-cutline',
        input_shp,
        input_raster,
        output_file
    ]
    # print output_file
    try:
        # log.info(args)
        log.info(' '.join(args))
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
        return output_file
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)


output_file = by_shp('/media/vortex/LaCie/nena/ndvi_anomaly/ndvi_anomaly_1km_mod13a3_200803_3857.geotiff', '/media/vortex/LaCie/nena/gaul1/output/aio/shape.shp')
# # print "END!!!"
print output_file