import os
import fiona
from shutil import copyfile
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_folder, get_filename


log = logger(__file__)

# TODO: move to geobricks_gis_vector library


# TODO: this can be optimized if needed to to don't create always the same shapefile in output
def cut_shp(input_shp, filter, output_path=None):

    if output_path is None:
        output_path = create_folder()

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # TODO: create the n shapefiles for each gaul1 selected
    # TODO: check if they are already available
    # output_base_path = os.path.join(output_path, type)
    # if not os.path.exists(output_base_path):
    #     os.mkdir(output_base_path)

    output_file = os.path.join(output_path, "shape.shp")

    with fiona.collection(input_shp, 'r') as source:
        # The output has the same schema
        schema = source.schema.copy()

        # write a new shapefile
        # TODO: dinamic projection
        with fiona.collection(output_file, 'w',
                              crs=source.crs,
                              driver=source.driver,
                              schema=schema) as output:

            # column is the property in the shapefile
            filter_property = filter['column'].upper()
            filter_codes = filter['codes']

            for f in source:
                try:
                    if f['properties'][filter_property] in filter_codes:
                        output.write(f)
                except Exception, e:
                    log.error(e)


    # TODO: check why fiona doesn't create a proper .prj file from the source one
    # dirty fix to that issue
    original_prj = os.path.join(os.path.dirname(input_shp), get_filename(input_shp) + '.prj')
    destination_prj = os.path.join(os.path.dirname(output_file), get_filename(output_file) + '.prj')
    copyfile(original_prj, destination_prj)

    return output_file
