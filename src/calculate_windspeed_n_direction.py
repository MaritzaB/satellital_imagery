import xarray as xr
import numpy as np
import rioxarray

# Leer el archivo NetCDF con componentes del viento
dir = 'data/2014/01/'
wind = f'{dir}cmems_obs-wind_glo_phy_my_l4_P1M_201401.nc'
wind_data = xr.open_dataset(wind, engine='netcdf4')
wind_data = wind_data.rename({'latitude': 'lat', 'longitude': 'lon'})

# Extraer las componentes del viento
u = wind_data.eastward_wind
v = wind_data.northward_wind

# Calcular la magnitud del viento (velocidad)
wind_speed = np.sqrt(u**2 + v**2)
wind_speed = wind_speed.squeeze()

# Calcular la dirección del viento en radianes
wind_direction_radians = np.arctan2(v, u)

# Oceanographic Convention: Convertir radianes a grados (hacia dónde va el viento)
wind_direction_ocean = np.degrees(wind_direction_radians)  # Convertir a grados
wind_direction_ocean = (wind_direction_ocean + 360) % 360  # Asegurar el rango de 0-360

# Meteorological Convention: Convertir radianes a grados (de dónde viene el viento)
wind_direction_meteo = (np.degrees(wind_direction_radians) + 180) % 360  # Ajustar 180° para dirección meteorológica

# Renombrar para guardar en GeoTIFF
wind_speed = wind_speed.rename('wind_speed')
wind_direction_ocean = wind_direction_ocean.rename('wind_direction_ocean')
wind_direction_meteo = wind_direction_meteo.rename('wind_direction_meteo')

# Establecer las dimensiones espaciales y el CRS (WGS84)
wind_speed.rio.set_spatial_dims('lon', 'lat', inplace=True)
wind_speed.rio.write_crs("EPSG:4326", inplace=True)

wind_direction_ocean.rio.set_spatial_dims('lon', 'lat', inplace=True)
wind_direction_ocean.rio.write_crs("EPSG:4326", inplace=True)

wind_direction_meteo.rio.set_spatial_dims('lon', 'lat', inplace=True)
wind_direction_meteo.rio.write_crs("EPSG:4326", inplace=True)

# Guardar la magnitud y las direcciones del viento como GeoTIFF
wind_speed.rio.to_raster(f'{dir}wind_speed_resampled.tif')
wind_direction_ocean.rio.to_raster(f'{dir}wind_direction_ocean_resampled.tif')
wind_direction_meteo.rio.to_raster(f'{dir}wind_direction_meteo_resampled.tif')


