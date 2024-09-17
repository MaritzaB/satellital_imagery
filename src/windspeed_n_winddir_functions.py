import xarray as xr
import numpy as np
import rioxarray

def extract_u_v(data):
    '''
    Extrae las componentes este-oeste (u) y norte-sur (v) del viento de un
    archivo NetCDF de datos de viento.
    '''
    wind_data = xr.open_dataset(data, engine='netcdf4')
    wind_data = wind_data.rename({'latitude': 'lat', 'longitude': 'lon'})
    u = wind_data.eastward_wind
    v = wind_data.northward_wind
    return u, v


def calculate_wind_speed(u, v):
    '''
    Calcula la magnitud de la velocidad del viento a partir de las componentes
    este-oeste (u) y norte-sur (v) del viento.
    '''
    wind_speed = np.sqrt(u**2 + v**2)
    wind_speed = wind_speed.squeeze()
    wind_speed = wind_speed.rename('wind_speed')
    return wind_speed


def calculate_wind_direction(u, v):
    '''
    Calcula la dirección del viento de acuerdo a la convención oceanográfica,
    que describe la dirección haca dónde se mueve el viento (no de dónde viene).
    En la convención oceanográfica, el viento del norte es 0° y aumenta en
    sentido horario.
    La función tiene como entrada las componentes u y v del viento y devuelve la
    dirección del viento en grados (0-360).
    Parametros:
    - u: componente este - oeste del viento, en m/s.
    - v: componente norte - sur del viento, en m/s.
    '''
    wind_direction_radians = np.arctan2(v, u)
    wind_direction = np.degrees(wind_direction_radians)
    wind_direction = (wind_direction + 360) % 360
    wind_direction = wind_direction.squeeze()
    wind_direction = wind_direction.rename('wind_direction_ocean')
    return wind_direction


def write_raster(dataarray, output_file, crs="EPSG:4326"):
    """
    Escribe un DataArray en formato raster GeoTIFF.

    Parámetros:
    - dataarray: Un `xarray.DataArray` que contiene los datos raster (por
    ejemplo, velocidad o dirección del viento).
    - output_file: Ruta donde se guardará el archivo GeoTIFF (incluyendo el
    nombre y la extensión .tif).
    - crs: Código EPSG del sistema de referencia de coordenadas (por defecto
    "EPSG:4326" para WGS 84).
    """
    dataarray.rio.set_spatial_dims('lon', 'lat', inplace=True)
    dataarray.rio.write_crs(crs, inplace=True)
    dataarray.rio.to_raster(output_file)


# Función de flujo principal
def calculate_windspeed_n_direction(wind_file, output_dir):
    """
    Calcula la velocidad y dirección del viento a partir de las componentes
    este-oeste (u) y norte-sur (v) del viento, y guarda los resultados en
    archivos GeoTIFF.

    Parámetros:
    - wind_file: Ruta al archivo NetCDF que contiene los datos de viento.
    - output_dir: Directorio donde se guardarán los archivos GeoTIFF.
    """
    u, v = extract_u_v(wind_file)
    wind_speed = calculate_wind_speed(u, v)
    wind_direction = calculate_wind_direction(u, v)
    write_raster(wind_speed, f'{output_dir}/wind_speed.tif')
    write_raster(wind_direction, f'{output_dir}/wind_direction.tif')

