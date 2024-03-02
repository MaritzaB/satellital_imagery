import wget
from datetime import datetime
import os

def descargar_archivo(url, filename):
    try:
        print(url)
        wget.download(url, out=filename)
        print("\nDescarga completada.")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110  

def create_directory(year, month):
    directory = f'data/{year}/{month}'
    os.makedirs(directory, exist_ok=True)
    return directory
        
def get_sst_data(year, month):
    '''
    Source: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdHadISST.graph'
    Source2: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.graph'
    '''
    #src='https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdHadISST.nc?sst%'
    #url=f'{src}5B({year}-{month}-16T12:00:00Z)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Csst&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    src = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.nc?sst%'
    url = f'{src}5B({year}-{month}-16T00:00:00Z)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Csst&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    directory = create_directory(year, month)
    filename = f'{directory}/{year}_{month}_jplMURSST41_.nc'
    descargar_archivo(url, filename)
    
def get_wind_data(year, month, dist_surface=10):
    '''
    Source: FNMOC 10m Surface Winds, 360x181, Monthly, Lon+/-180
    https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind10_LonPM180.graph
    
    Source: FNMOC 20m Surface Winds, 360x181, Monthly, Lon+/-180
    https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind20_LonPM180.graph
    
    Source: Global Ocean Monthly Mean Sea Surface Wind and Stress from
    Scatterometer and Model --BUENO-- 0.25 Degree
    https://data.marine.copernicus.eu/product/WIND_GLO_PHY_CLIMATE_L4_MY_012_003/files?subdataset=cmems_obs-wind_glo_phy_my_l4_P1M_202211
    '''
    latitude_ranges = f'%5D%5B({min_lat}):({max_lat})'
    longitude_ranges = f'%5D%5B({min_lon}):({max_lon})'
    src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind{dist_surface}_LonPM180.nc'
    url = f'{src}?u_mean%5B({year}-{month}-01T00:00:00Z){latitude_ranges}{longitude_ranges}%5D,v_mean%5B({year}-{month}-01T00:00:00Z){latitude_ranges}{longitude_ranges}%5D&.draw=vectors&.vars=longitude%7Clatitude%7Cu_mean%7Cv_mean&.color=0x000000&.bgColor=0xffccccff'
    directory = create_directory(year, month)
    filename = f'{directory}/{year}_{month}_FNMOC_10m_Surface_Winds.nc'
    descargar_archivo(url, filename)
        
def get_chlc_data(year, month):
    '''
    Source: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.graph?chlor_a'
    '''
    src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.nc?chlor_a'
    url = f'{src}%5B({year}-{month}-01T12:00:00Z)%5D%5B(0.0)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Cchlor_a&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    print(url)
    directory = create_directory(year, month)
    filename = f'{directory}/{year}_{month}_NESDIS_VHNSQ_chla.nc'
    descargar_archivo(url, filename)

def process_data(process_function, years, months):
    for year in years:
        for month in months:
            process_function(year, month)
            # pause = input('Press enter to continue: ')

def process_chlc_data(year, month):
    get_chlc_data(year, month)

def process_wind_data(year, month):
    get_wind_data(year, month)

def process_sst_data(year, month):
    get_sst_data(year, month)

data_processing_functions = {
    'chlc': process_chlc_data,
    'wind': process_wind_data,
    'sst': process_sst_data
}

years = [2014, 2015, 2016, 2017, 2018]
months = [f'{i:02d}' for i in range(1, 13) ]
datatype = ['chlc', 'sst']

for data in datatype:
    if data in data_processing_functions:
        process_data(data_processing_functions[data], years, months)
