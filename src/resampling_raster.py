import xarray as xr
import rioxarray as rxr
import glob as glob
import os
from rasterio.warp import reproject, Resampling, calculate_default_transform
import rasterio

def netcdf_to_tif(nc_file, *variables):
    """
    Convert netCDF file to tif.
    If multiple variables are provided, each variable will be converted to a
    separate tif.
    """
    ds = xr.open_dataset(nc_file)
    filename = os.path.basename(nc_file)
    processed_dir = os.path.dirname(nc_file) + '/processed'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    for var in variables:
        if var == 'sst':
            da = ds[var]
            da.rio.set_spatial_dims('longitude', 'latitude', inplace=True)
        elif var == 'chlor_a':
            da = ds[var].isel(altitude=0)
            da.rio.set_spatial_dims('longitude', 'latitude', inplace=True)
            if 'grid_mapping' in da.attrs:
                da.attrs.pop('grid_mapping')
        else:
            da = ds[var]
            da.rio.set_spatial_dims('lon', 'lat', inplace=True)
        crs = 'EPSG:4326'
        da.rio.write_crs(crs, inplace=True)
        da.rio.to_raster(f'{processed_dir}/{filename[:-3]}_{var}.tif')
        print(f'Converted {var} to tif: {processed_dir}/{filename[:-3]}_{var}.tif')
    ds.close()

def reproj_match(infile, match, outfile):
    """Reproject a file to match the shape and projection of existing raster. 
    
    Parameters
    ----------
    infile : (string) path to input file to reproject
    match : (string) path to raster with desired shape and projection 
    outfile : (string) path to output file tif
    """
    # open input
    with rasterio.open(infile) as src:
        src_transform = src.transform
        
        # open input to match
        with rasterio.open(match) as match:
            dst_crs = match.crs
            
            # calculate the output transform matrix
            dst_transform, dst_width, dst_height = calculate_default_transform(
                src.crs,     # input CRS
                dst_crs,     # output CRS
                match.width,   # input width
                match.height,  # input height 
                *match.bounds,  # unpacks input outer boundaries (left, bottom, right, top)
            )

        # set properties for output
        dst_kwargs = src.meta.copy()
        dst_kwargs.update({"crs": dst_crs,
                           "transform": dst_transform,
                           "width": dst_width,
                           "height": dst_height,
                           "nodata": 0})
        print("Coregistered to shape:", dst_height,dst_width,'\n Affine',dst_transform)
        # open output
        with rasterio.open(outfile, "w", **dst_kwargs) as dst:
            # iterate through bands and write using reproject function
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)

def get_filenames(year, month):
    directory = f'data/{year}/{month}'
    sst_file = f'{directory}/{year}_{month}_jplMURSST41__.tif'
    chla_file = f'{directory}/{year}_{month}_NESDIS_VHNSQ_chla.tif'
    processed_dir = f'{directory}/processed'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    out_sst = f'{processed_dir}/{year}_{month}_jplMURSST41_reproj.tif'
    out_chla = f'{processed_dir}/{year}_{month}_NESDIS_VHNSQ_chla_reproj.tif'
    return sst_file, chla_file, out_sst, out_chla

def wind_to_tif(years, months):
    for year in years:
        for month in months:
            wind_file = f'data/{year}/{month}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}_clipped.nc'
            netcdf_to_tif(wind_file, 'eastward_wind', 'northward_wind')

def chlc_to_tif(years, months):
    for year in years:
        for month in months:
            chlc_file = f'data/{year}/{month}/{year}_{month}_NESDIS_VHNSQ_chla_chlor_a.nc'
            netcdf_to_tif(chlc_file, 'chlor_a')
            
def sst_to_tif(years, months):
    for year in years:
        for month in months:
            sst_file = f'data/{year}/{month}/{year}_{month}_jplMURSST41__sst.nc'
            netcdf_to_tif(sst_file, 'sst')

def reprojection(years, months):
    for year in years:
        for month in months:
            print(f'Processing {year}-{month}')
            sst_file, chla_file, out_sst, out_chla = get_filenames(year, month)
            reproj_match(sst_file, chla_file, out_sst)
            reproj_match(chla_file, sst_file, out_chla)

years = [year for year in range(2014, 2019)]
months = [f'{i:02d}' for i in range(1, 13) ]

# Create tif files
wind_to_tif(years, months)
sst_to_tif(years, months)
chlc_to_tif(years, months)

# Resample tif files
reprojection(years, months)

def clean_processed():
    for year in years:
        for month in months:
            directory = f'data/{year}/{month}'
            processed_dir = f'{directory}/processed'
            for file in glob.glob(f'{processed_dir}/*'):
                os.remove(file)
            os.rmdir(processed_dir)

# Uncomment next line to clean processed directory
#clean_processed()