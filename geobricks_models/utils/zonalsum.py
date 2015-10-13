import rasterio
from numpy import sum

# TODO calculate zonalsums for each gaul1
def zonalsum(input_raster, scale_factor=1):

    with rasterio.open(input_raster) as r:

        r_data = r.read_band(1).astype(float).flatten()

        return sum(r_data) * scale_factor


print zonalsum('/media/vortex/LaCie/nena/calc.tif', 12)
# print zonalsum('/media/vortex/LaCie/nena/calc.tif', 11)