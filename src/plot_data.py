import xarray as xr
import rioxarray as rxr
import netCDF4 as nc
import numpy as np
import pandas as pd
# Plot the data
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap

# Plot sea surface temperature, chlorophyll-a, and sea wind speed in three
# different subplots

# Load the data
dir = 'data/2014/01/'
sst = f'{dir}2014_01_jplMURSST41_.nc'
chla = f'{dir}2014_01_NESDIS_VHNSQ_chla.nc'
wind = f'{dir}cmems_obs-wind_glo_phy_my_l4_P1M_201401.nc'

# Open the data with xarray
sst_data = rxr.open_rasterio(sst)
chla_data = xr.open_dataset(chla)
wind_data = xr.open_dataset(wind)

# Extract the data
chla_data = chla_data['chlor_a'].isel(altitude=0)
chla_data = chla_data.rename({'latitude': 'y', 'longitude': 'x'})
wind_data = wind_data.rename({'latitude': 'lat', 'longitude': 'lon'})

print(f'SST data shape: {sst_data.shape}')
print(f'Chlorophyll-a data shape: {chla_data.shape}')
print(f'Wind data shape: {wind_data.eastward_wind.shape}')

# Define bounding box
min_lat, max_lat = 23, 55
min_lon, max_lon = -163, -110
zoom_min_lat, zoom_max_lat = 30.5, 30.9
zoom_min_lon, zoom_max_lon = -123, -122.6

# Plot the data
fig, axs = plt.subplots(3, 1, figsize=(20, 30))
inset_lims = [0.68, 0.5, 0.4, 0.4]

# Plot sea surface temperature
m = Basemap(projection='cyl', resolution='l', ax=axs[0], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
sst = sst_data.squeeze()
x, y = sst_data.x, sst_data.y
cs = m.pcolormesh(x, y, sst, cmap='jet', latlon=True, vmin=3, vmax=28)
#m.fillcontinents(color='#ebe7d5', lake_color='gray') 
#m.drawcoastlines(color='gray')
#m.drawcountries(color='gray')
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
# Zoom in on the Pacific Ocean
axins = axs[0].inset_axes(inset_lims, xlim=(zoom_min_lon, zoom_max_lon), ylim=(zoom_min_lat, zoom_max_lat))
axins.imshow(sst, cmap='jet', vmin=3, vmax=28, extent=[sst_data.x.min(), sst_data.x.max(), sst_data.y.min(), sst_data.y.max()])
axs[0].indicate_inset_zoom(axins, edgecolor="black")

## Plot chlorophyll-a concentration on the second subplot
m = Basemap(projection='cyl', resolution='l', ax=axs[1], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
#m.fillcontinents(color='#ebe7d5', lake_color='gray')
#m.drawcoastlines(color='gray')
#m.drawcountries(color='gray')
x, y = chla_data.x, chla_data.y
chla = chla_data.squeeze()
cs = m.pcolormesh(x, y, chla, cmap='viridis', latlon=True, norm=LogNorm( vmin=0.01, vmax=10))
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
# Zoom in on the Pacific Ocean
axins = axs[1].inset_axes(inset_lims, xlim=(zoom_min_lon, zoom_max_lon), ylim=(zoom_min_lat, zoom_max_lat))
axins.imshow(chla_data.squeeze(), cmap='viridis', norm=LogNorm(vmin=0.01, vmax=10), extent=[sst_data.x.min(), sst_data.x.max(), sst_data.y.min(), sst_data.y.max()])
axs[1].indicate_inset_zoom(axins, edgecolor="black")

# Plot sea wind speed and direction on the third subplot
axs[2].set_title('Mean Sea Wind Speed (m/s) - January 2014', fontsize=20)
axs[2].set_xlabel('Longitude', fontsize=18, labelpad=50)
axs[2].set_ylabel('Latitude', fontsize=18, labelpad=80)
m = Basemap(projection='cyl', resolution='l', ax=axs[2], llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
#m.fillcontinents(color='#ebe7d5', lake_color='gray')
#m.drawcoastlines(color='gray')
#m.drawcountries(color='gray')
# Calculate the wind speed
u = wind_data.eastward_wind
v = wind_data.northward_wind
wind_speed = np.sqrt(u**2 + v**2)
wind_speed = wind_speed.squeeze()
x, y = wind_data.lon, wind_data.lat
cs2 = m.pcolormesh(x, y, wind_speed, cmap='autumn_r', latlon=True)
#uproj, vproj = m.rotate_vector(u.squeeze(), v.squeeze(), wind_data.lon, wind_data.lat, returnxy=False)
#m.quiver(x, y, uproj, vproj, scale=250, width=0.0015, headwidth=1, headlength=2, headaxislength=2, color='black')
cbar = m.colorbar(cs2, location='right', pad="5%", size="5%", ticks=[speed for speed in range(0, 20, 2)])
cbar.set_label('Wind Speed (m/s)', fontsize=15)
m.drawmeridians(np.arange(min_lon, max_lon, 5), labels=[0, 0, 0, 1], color='gray', fontsize=15, dashes=[4, 4])
m.drawparallels(np.arange(min_lat, max_lat, 10), labels=[1, 0, 0, 0], color='gray', fontsize=15, dashes=[4, 4])
axs[2].set_aspect('auto')
axs[2].set_xlim(min_lon, max_lon)
axs[2].set_ylim(min_lat, max_lat)
axs[2].grid()
axins = axs[2].inset_axes(inset_lims, xlim=(zoom_min_lon, zoom_max_lon), ylim=(zoom_min_lat, zoom_max_lat))
axins.imshow(wind_speed, cmap='autumn_r', extent=[min_lon, max_lon, min_lat, max_lat])
axs[2].indicate_inset_zoom(axins, edgecolor="black")

plt.tight_layout()
plt.savefig(f'{dir}oceanographic_raw_data.png')

