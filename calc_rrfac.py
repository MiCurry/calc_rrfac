import argparse
import numpy as np
from netCDF4 import Dataset


def sphere_distance(lat1, lon1, lat2, lon2, radius, **kwargs):
    """ Calculate the sphere distance between point1 and point2. 

    lat1 - Float - Radians - -pi:pi
    lon1 - Float - Radians - 0:2*pi
    lat2 - Float - Radians - -pi:pi
    lon2 - Float - Radians - 0:2*pi
    radius - Radius of the earth (or sphere) - Units can be ignored

    """ 
    return (2 * radius * np.arcsin(
                         np.sqrt(
                         np.sin(0.5 * (lat2 - lat1))**2
                       + np.cos(lat1) 
                       * np.cos(lat2) 
                       * np.sin(0.5 * (lon2 - lon1))**2)))

# Calculate rrfac for a scrip file

parser = argparse.ArgumentParser()
parser.add_argument('scrip',
                    help='SCRIP file',
                    type=str)

args = parser.parse_args()

scrip = Dataset(args.scrip, 'r+')

grid_size = scrip.dimensions['grid_size'].size
grid_area = scrip.variables['grid_area'][:]

# Calculate rrfac using grid_area
rrfac = np.array(grid_size)
max_area = max(grid_area)
rrfac = max_area / grid_area[:]
rrfac = np.sqrt(rrfac)
max_rrfac = max(rrfac)

if not 'rrfac' in scrip.variables:
    scrip.createVariable('rrfac', 'd', dimensions=('grid_size',))

scrip.variables['rrfac'].setncattr('max_rrfac', max_rrfac)
scrip.variables['rrfac'][:] = rrfac

print("MAX rrfac - Needed by Topo tool: ", max_rrfac)

scrip.close()
