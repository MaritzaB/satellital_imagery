#!/usr/bin/env python

import xarray as xr
import glob as glob
import os

def clip_netCDF(input_file):
    ds = xr.open_dataset(input_file)

    # Define the region of interest
    min_lat = 23
    max_lat = 55
    min_lon = -163
    max_lon = -110
    
    # Clip the data to the region of interest
    ds_clipped = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))

    # Save the clipped data to a new netCDF file
    output_file = input_file[:-3] + '_clipped.nc'
    print(output_file)
    ds_clipped.to_netcdf(output_file)

    ds.close()
    ds_clipped.close()
    
    # Remove the original file
    os.remove(input_file)

dataset = glob.glob('src/data/chlc/2014/02/*.nc')

for file in dataset:
    print(file)
    clip_netCDF(file)
