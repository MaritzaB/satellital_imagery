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
        #print(f'Writing {var} to raster')
        CRS = 'EPSG:4326'
        ds[var].rio.write_crs(CRS).rio.to_raster(f'{new_directory}{var}.tif')
      
def verify_shape(input_shape, reference_shape):
    if input_shape == reference_shape:
        return True
    else:
        return False

def resample_sst_raster(input_file, reference_file, new_directory):
    CRS = 'EPSG:4326'
    reference_ds = rxr.open_rasterio(reference_file)
    reference_ds = reference_ds.rio.write_crs(CRS)
    input_ds = rxr.open_rasterio(input_file)
    input_ds = input_ds.rio.write_crs(CRS)
    reprojected = input_ds.rio.reproject_match(reference_ds, resampling=Resampling.average)
    reprojected = reprojected.rio.write_crs(CRS)
    output_file = input_ds.name + '_resampled.tif'
    if verify_shape(reprojected.shape, reference_ds.shape):
        reprojected.rio.to_raster(f'{new_directory}{output_file}')
        #print('SST and Wind shapes match')
    else:
        print('SST and Wind shapes doesnt match')
        return False
    
def resample_chla_raster(input_file, reference_file, new_directory):
    CRS = 'EPSG:4326'
    reference_ds = rxr.open_rasterio(reference_file)
    reference_ds = reference_ds.rio.write_crs(CRS)
    input_ds = xr.open_dataset(input_file)
    input_ds = input_ds['chlor_a'].isel(altitude=0)
    input_ds = input_ds.rio.write_crs(CRS)
    reprojected = input_ds.rio.reproject_match(reference_ds, resampling=Resampling.average)
    reprojected.attrs.pop('grid_mapping', None)
    reprojected = reprojected.rio.write_crs(CRS)
    output_file = input_ds.name + '_resampled.tif'
    if verify_shape(reprojected.shape, reference_ds.shape):
        reprojected.rio.to_raster(f'{new_directory}{output_file}')
        #print('Chla and Wind shapes match')
    else:
        print('Chla and Wind shapes doesnt match')
        return False

def downsample_all_files(year, month):
    dir = f'data/{year}/{month}/'
    wind_file = f'{dir}cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}.nc'
    sst_file = f'{dir}{year}_{month}_jplMURSST41_.nc'
    chla_file = f'{dir}{year}_{month}_NESDIS_VHNSQ_chla.nc'
    new_dir = f'resampled_data/{year}/{month}/'
    match_file = f'{new_dir}eastward_wind.tif'
    make_dir(new_dir)
    write_raster(wind_file, new_dir)
    resample_sst_raster(sst_file, match_file, new_dir)
    resample_chla_raster(chla_file, match_file, new_dir)
    
years = [ f'{i:04d}' for i in range(2014, 2018)]
months = [f'{i:02d}' for i in range(1, 13)]

for year in years:
    for month in months:
        print(f'Processing {year}-{month}')
        downsample_all_files(year, month)
