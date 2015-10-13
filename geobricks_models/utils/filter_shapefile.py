import os
import fiona
from geobricks_common.core.log import logger

log = logger(__file__)


def cut_shp(input_shp, output_path, filter, type):

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # TODO: create the n shapefiles for each gaul1 selected
    # TODO: check if they are already available
    output_base_path = os.path.join(output_path, type)

    if not os.path.exists(output_base_path):
        os.mkdir(output_base_path)

    output_file = os.path.join(output_base_path, "shape.shp")

    #output_base_path = os.path.join(output_path, "gaul1")
    # TODO: for each "code" in codes create a gaul1

    with fiona.collection(input_shp, 'r') as source:
        # The output has the same schema
        schema = source.schema.copy()

        # write a new shapefile
        # TODO: dinamic projection
        with fiona.collection(output_file, 'w',
                              crs=source.crs,
                              driver=source.driver,
                              schema=schema) as output:

            filter_property = filter['property'].upper()
            filter_codes = filter['codes']

            for f in source:
                try:
                    if f['properties'][filter_property] in filter_codes:
                        print f['properties'][filter_property]
                        output.write(f)
                except Exception, e:
                    log.error(e)

    return output_file



# filter = {
#     "shapefile_name" ??
#     "property": "adm1_code",
#     "codes": [61525, 2755]
# }
#
# output_files = cut_shp(
#     '/media/vortex/LaCie/nena/gaul1/',
#     '/media/vortex/LaCie/nena/gaul1/output',
#     filter,
#     'aoi'
# )