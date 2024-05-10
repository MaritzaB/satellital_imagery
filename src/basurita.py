import xarray as xr
import rioxarray as rxr
import netCDF4 as nc
import numpy as np
# Plot the data
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap

# Tambien se puede resamplear la data con rioxarray
# En este caso estamos haciendo un upsampling de los datos de temperatura

input_data = 'data/2014/01/processed/cmems_obs-wind_glo_phy_my_l4_P1M_201401_clipped_eastward_wind.tif'
match_data = 'data/2014/01/processed/2014_01_jplMURSST41__sst.tif'

match_data = rxr.open_rasterio(match_data)
input_data = rxr.open_rasterio(input_data)

print(f'Match data shape: {match_data.shape}')
print(f'Input data shape: {input_data.shape}')
print(f'Match projection: {match_data.rio.crs}')

# broadcast the wind data to the same shape as the other data
print(f'Broadcasting wind data to the same shape as the other data')
print(f'Before broadcasting: Match shape: {match_data.shape}, Input shape: {input_data.shape}')
match_data = match_data.rio.reproject_match(input_data)
print(f'After broadcasting: Match shape: {match_data.shape}, Input shape: {input_data.shape}')

# Write the data to a new file
output_file = 'data/2014/01/processed/2014_01_jplMURSST41_reproj_with_rioxarray.tif'
match_data.rio.to_raster(output_file)

