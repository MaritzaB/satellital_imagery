import wget
import copernicusmarine as cm
from datetime import datetime
import os

def descargar_archivo(url, filename):
    try:
        print(url)
        wget.download(url, out=filename)
        print("\nDescarga completada.")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

min_lat = 10
max_lat = 61
min_lon = -179
max_lon = -110

def create_directory(year, month):
    directory = f'data/{year}/{month}'
    os.makedirs(directory, exist_ok=True)
    return directory
        
def get_sst_data(year, month):
    '''
    Source: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.graph'
    '''
    src = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.nc?sst%'
    url = f'{src}5B({year}-{month}-16T00:00:00Z)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Csst&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    directory = create_directory(year, month)
    filename = f'{directory}/{year}_{month}_jplMURSST41_.nc'
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
    
def get_wind_data(year, month):
    cm.subset(
        dataset_id="cmems_obs-wind_glo_phy_my_l4_P1M",
        dataset_version="202211",
        variables=["eastward_stress", "eastward_stress_bias", "eastward_stress_sdd", "eastward_wind", "eastward_wind_bias", "eastward_wind_sdd", "northward_stress", "northward_stress_bias", "northward_stress_sdd", "northward_wind", "northward_wind_bias", "northward_wind_sdd", "number_of_observations"],
        minimum_longitude=min_lon,
        maximum_longitude=max_lon,
        minimum_latitude=min_lat,
        maximum_latitude=max_lat,
        start_datetime=f"{year}-{month}-01T00:00:00",
        end_datetime=f"{year}-{month}-01T00:00:00",
        output_filename=f"data/{year}/{month}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}.nc"
    )
    


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
datatype = ['wind']

for data in datatype:
    if data in data_processing_functions:
        process_data(data_processing_functions[data], years, months)
