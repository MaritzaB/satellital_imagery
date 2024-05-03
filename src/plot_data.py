import xarray as xr
import rioxarray as rxr
import netCDF4 as nc
import numpy as np
# Plot the data
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap

# Plot sea surface temperature, chlorophyll-a, and sea wind speed in three
# different subplots

# Load the data
sst = 'data/2014/01/processed/resampled_data/2014_01_jplMURSST41_reproj.tif'
chla = 'data/2014/01/processed/resampled_data/2014_01_NESDIS_VHNSQ_chla_reproj.tif'
u_wind = 'data/2014/01/processed/cmems_obs-wind_glo_phy_my_l4_P1M_201401_clipped_eastward_wind.tif'
v_wind = 'data/2014/01/processed/cmems_obs-wind_glo_phy_my_l4_P1M_201401_clipped_northward_wind.tif'

# Open the data with xarray
sst_data = rxr.open_rasterio(sst)
chla_data = rxr.open_rasterio(chla)
u_wind_data = rxr.open_rasterio(u_wind)
v_wind_data = rxr.open_rasterio(v_wind)

print(f'SST data shape: {sst_data.shape}')
print(f'Chlorophyll-a data shape: {chla_data.shape}')
print(f'Eastward wind data shape: {u_wind_data.shape}')
print(f'Northward wind data shape: {v_wind_data.shape}')
print(f'SST projection: {sst_data.rio.crs}')

# Define bounding box
min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110

# Plot the data
fig, axs = plt.subplots(3, 1, figsize=(20, 40))
# Plot sea surface temperature
m = Basemap(projection='cyl', resolution='l', ax=axs[0], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
cs = m.pcolormesh(sst_data.x, sst_data.y, sst_data.squeeze(), cmap='jet', latlon=True)
m.fillcontinents(color='#ebe7d5', lake_color='gray') 
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawmeridians(np.arange(min_lon, max_lon, 5), labels=[0, 0, 0, 1], color='gray', fontsize=15, dashes=[4, 4])
m.drawparallels(np.arange(min_lat, max_lat, 10), labels=[1, 0, 0, 0], color='gray', fontsize=15, dashes=[4, 4])
cbar = m.colorbar(cs, location='right', pad="5%", size="5%", ticks=[temp for temp in range(0, 35, 5)])
cbar.set_label('SST (°C)', fontsize=15)
axs[0].set_title('Mean Sea Surface Temperature (°C) - January 2014', fontsize=20)
axs[0].set_xlabel('Longitude', fontsize=18, labelpad=50)
axs[0].set_ylabel('Latitude', fontsize=18, labelpad=80)
axs[0].set_aspect('auto')
axs[0].set_xlim(min_lon, max_lon)
axs[0].set_ylim(min_lat, max_lat)
axs[0].grid()

# Plot chlorophyll-a concentration on the second subplot
m = Basemap(projection='cyl', resolution='l', ax=axs[1], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
cs = m.pcolormesh(chla_data.x, chla_data.y, chla_data.squeeze(), cmap='viridis', latlon=True, norm=LogNorm( vmin=0.01, vmax=10 ))
m.fillcontinents(color='#ebe7d5', lake_color='gray')
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawmeridians(np.arange(min_lon, max_lon, 5), labels=[0, 0, 0, 1], color='gray', fontsize=15, dashes=[4, 4])
m.drawparallels(np.arange(min_lat, max_lat, 10), labels=[1, 0, 0, 0], color='gray', fontsize=15, dashes=[4, 4])
cbar = m.colorbar(cs, location='right', pad="5%", size="5%", ticks= [0.01, 0.1, 1, 10])
cbar.set_label('Chlorophyll-a (mg/m³)', fontsize=15)
axs[1].set_title('Mean Chlorophyll-a Concentration (mg/m³) - January 2014', fontsize=20)
axs[1].set_xlabel('Longitude', fontsize=18, labelpad=50)
axs[1].set_ylabel('Latitude', fontsize=18, labelpad=80)
axs[1].set_aspect('auto')
axs[1].set_xlim(min_lon, max_lon)
axs[1].set_ylim(min_lat, max_lat)
axs[1].grid()

# Plot sea wind speed and direction on the third subplot
axs[2].set_title('Mean Sea Wind Speed (m/s) - January 2014', fontsize=20)
axs[2].set_xlabel('Longitude', fontsize=18, labelpad=50)
axs[2].set_ylabel('Latitude', fontsize=18, labelpad=80)
m = Basemap(projection='cyl', resolution='l', ax=axs[2], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)

plt.savefig('data/2014/01/processed/sst.png')

