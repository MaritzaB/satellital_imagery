import xarray as xr
import rioxarray as rxr
import os
from rasterio.enums import Resampling
from windspeed_n_winddir_functions import calculate_windspeed_n_direction


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_raster(netcdf, new_directory):
    ds = rxr.open_rasterio(netcdf)
    for var in ds.data_vars:
        print(f'Writing {var} to raster')
        CRS = 'EPSG:4326'
        ds[var].rio.write_crs(CRS).rio.to_raster(f'{new_directory}/{var}.tif')
      

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
        reprojected.rio.to_raster(f'{new_directory}/{output_file}')
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
        reprojected.rio.to_raster(f'{new_directory}/{output_file}')
        #print('Chla and Wind shapes match')
    else:
        print('Chla and Wind shapes doesnt match')
        return False


def downsample_all_files(year, month):
    raw_data_directory = f'data/{year}/{month}'
    wind_file = f'{raw_data_directory}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}.nc'
    sst_file = f'{raw_data_directory}/{year}_{month}_jplMURSST41_.nc'
    chla_file = f'{raw_data_directory}/{year}_{month}_NESDIS_VHNSQ_chla.nc'
    output_directory = f'resampled_data/{year}/{month}'
    match_file = f'{output_directory}/wind_speed.tif'
    make_dir(output_directory)
    calculate_windspeed_n_direction(wind_file, output_directory)
    resample_sst_raster(sst_file, match_file, output_directory)
    resample_chla_raster(chla_file, match_file, output_directory)


years = [ f'{i:04d}' for i in range(2014, 2019)]
months = [f'{i:02d}' for i in range(1, 4)]


for year in years:
    for month in months:
        print(f'Processing {year}-{month}')
        downsample_all_files(year, month)

