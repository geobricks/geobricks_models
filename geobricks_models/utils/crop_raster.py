import fiona
import subprocess
from pyproj import Proj, transform
import rasterio
from geobricks_common.core.filesystem import create_tmp_filename
from geobricks_common.core.log import logger

log = logger(__file__)

# TODO: check if raster and shp are of the same projection
def by_shp(input_raster, input_shp):

    # log.info('Cropping: ' + input_raster + ' by ' + input_shp)

    output_file = crop_by_shapefile_bbox(input_raster, input_shp)

    return crop_by_shapefile_cutline(output_file, input_shp)


def crop_by_shapefile_bbox(input_raster, input_shp):

    # log.info('Crop_by_shapefile_bbox: ' + input_raster + ' by ' + input_shp)

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
        '-co',
        'COMPRESS=DEFLATE',
        '-cutline',
        input_shp,
        input_raster,
        output_file
    ]
    # print output_file
    try:
        # log.info(args)
        # log.info(' '.join(args))
        #TODO: handle subprocess Error (like that is not taken)
        proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
        return output_file
    except:
        stdout_value = proc.communicate()[0]
        raise Exception(stdout_value)



# def crop_by_rastrer_bbox(input_raster_to_cut, input_raster_cutter):
#
#     log.info('Crop_by_raster_bbox: ' + input_raster_to_cut + ' by ' + input_raster_cutter)
#
#     with rasterio.open(input_raster_cutter) as raster_cutter:
#
#
#         west, south = -20037505.400, -24654637.153
#         east, north = 20033536.783,24650818.928
#
#         # maxlat, minlat, maxlon, minlon = shp.bounds
#         # west, south, east, north = shp.bounds
#
#         with rasterio.open(input_raster_to_cut) as raster_to_cut:
#
#             # TODO: check both crs if exists
#             # p_in = Proj(shp.crs)
#             # p_out = Proj(raster.meta['crs'])
#             #
#             # # transform bbox to the right coordinate system
#             # west, south = transform(p_in, p_out, west, south)
#             # east, north = transform(p_in, p_out, east, north)
#
#             from geobricks_common.core.filesystem import get_filename
#             # create tmp output file
#             output_file = '/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/' + get_filename(input_raster_to_cut) + '.tif'
#
#             args = [
#                 'gdalwarp',
#                 '-te',
#                 str(west),
#                 str(south),
#                 str(east),
#                 str(north),
#                 '-tr',
#                 str(7891.107164990120509),
#                 str(-7892.661450427384807),
#                 input_raster_to_cut,
#                 output_file
#             ]
#
#             try:
#                 # log.info(args)
#                 log.info(' '.join(args))
#                 print "TODO: use the line printed below, there is an error with args and tr"
#                 print ' '.join(args)
#                 #TODO: handle subprocess Error (like that is not taken)
#                 proc = subprocess.call(args, stdout=subprocess.PIPE, stderr=None)
#
#                 return output_file
#
#             except:
#                 stdout_value = proc.communicate()[0]
#                 raise Exception(stdout_value)
#
# print crop_by_rastrer_bbox('/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/bk/LST_6km_MYD11C3_201507_3857.tif', '/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/LST_6km_MYD11C3_201406_3857.tif')
# print crop_by_rastrer_bbox('/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/bk/LST_6km_MYD11C3_201508_3857.tif', '/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/LST_6km_MYD11C3_201406_3857.tif')
# print crop_by_rastrer_bbox('/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/bk/LST_6km_MYD11C3_201509_3857.tif', '/media/vortex/LaCie/LaCie/ECO_COUNTRIES/MYD11C3/LST_6km_MYD11C3_201406_3857.tif')