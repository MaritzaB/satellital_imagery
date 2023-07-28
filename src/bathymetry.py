from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

filename = 'data/GEBCO_27072023/gebco_2023_n32.0_s25.0_w-116.0_e-106.0.nc'
data = Dataset(filename, mode='r')
print(data.variables.keys())

elevation = data['elevation'][:]
lon = data['lon'][:]
lat = data['lat'][:]

elevation = np.float32(elevation)
elevation[elevation>=0] = np.nan

plt.pcolor(lon,lat,elevation)
plt.title('Batimetría Golfo de California')
plt.savefig('images/bathymetry.png')
