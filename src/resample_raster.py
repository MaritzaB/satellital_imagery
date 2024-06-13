import xarray as xr
import rioxarray as rxr
import os
from rasterio.enums import Resampling


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_raster(netcdf, new_directory):
    ds = rxr.open_rasterio(netcdf)
    for var in ds.data_vars:
        print(var)
        ds[var].rio.to_raster(f'{new_directory}{var}.tif')
      
def verify_shape(input_shape, reference_shape):
    if input_shape == reference_shape:
        return True
    else:
        return False

def resample_raster(input_file, reference_file, new_directory):
    input_ds = rxr.open_rasterio(input_file)
    reference_ds = rxr.open_rasterio(reference_file)
    CRS = 'EPSG:4326'
    input_ds = input_ds.rio.write_crs(CRS)
    reference_ds = reference_ds.rio.write_crs(CRS)
    reprojected = input_ds.rio.reproject_match(reference_ds, resampling=Resampling.average)
    reprojected = reprojected.rio.write_crs(CRS)
    output_file = input_ds.name + '_resampled.tif'
    print(output_file)
    if verify_shape(reprojected.shape, reference_ds.shape):
        reprojected.rio.to_raster(f'{new_directory}{output_file}')
        print('Shapes match')
    else:
        print('Shapes do not match')
        return False

year = '2014'
month = '01'
dir = f'data/{year}/{month}/'
wind_file = f'{dir}cmems_obs-wind_glo_phy_my_l4_P1M_201401.nc'
new_dir = f'resampled_data/{year}/{month}/'
match_file = f'{new_dir}eastward_wind.tif'
sst_file = f'{dir}2014_01_jplMURSST41_.nc'

make_dir(new_dir)
write_raster(wind_file, new_dir)
resample_raster(sst_file, match_file, new_dir)
