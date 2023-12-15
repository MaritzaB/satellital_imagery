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
        
def get_chlc_data(year, month):
    '''
    Source: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.graph?chlor_a'
    '''
    src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.nc?chlor_a'
    url = f'{src}%5B({year}-{month}-01T12:00:00Z)%5D%5B(0.0)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Cchlor_a&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    print(url)
    directory = f'chlc/{year}/{month}/'
    os.makedirs(directory, exist_ok=True)
    descargar_archivo(url, directory)

min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110

def get_wind_data(year, month, day, dist_surface=10):
    '''
    Source: FNMOC 10m Surface Winds, 360x181, Monthly, Lon+/-180
    https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind10_LonPM180.graph
    
    Source: FNMOC 20m Surface Winds, 360x181, Monthly, Lon+/-180
    https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind20_LonPM180.graph
    '''
    latitude_ranges = f'%5D%5B({min_lat}):({max_lat})'
    longitude_ranges = f'%5D%5B({min_lon}):({max_lon})'
    year_month = f'{year}-{month}-{day}T00:00:00Z'
    #src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdlasFnWind{dist_surface}_LonPM180.nc'
    #url =
    #f'{src}?u_mean%5B({year}-{month}-01T00:00:00Z){latitude_ranges}{longitude_ranges}%5D,v_mean%5B({year}-{month}-01T00:00:00Z){latitude_ranges}{longitude_ranges}%5D&.draw=vectors&.vars=longitude%7Clatitude%7Cu_mean%7Cv_mean&.color=0x000000&.bgColor=0xffccccff'
    ### NAVGEM 10m Surface Wind Lon+/-180
    src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdNavgem05D10mWind_LonPM180.nc'
    url = f'{src}?wnd_ucmp_height_above_ground%5B({year_month})%5D%5B(10.0){latitude_ranges}{longitude_ranges}%5D,wnd_vcmp_height_above_ground%5B({year_month})%5D%5B(10.0){latitude_ranges}{longitude_ranges}%5D&.draw=vectors&.vars=longitude%7Clatitude%7Cwnd_ucmp_height_above_ground%7Cwnd_vcmp_height_above_ground&.color=0x000000&.bgColor=0xffccccff'
    directory = f'wind/'
    file_name = f'{directory}/{year}{month}{day}_FNMOC_10m_Surface_Winds.nc'
    print(url)
    os.makedirs(directory, exist_ok=True)
    descargar_archivo(url, file_name)

years = [2014, 2015, 2016, 2017, 2018]
months = [f'{i:02d}' for i in range(1, 13) ]
days = [f'{i:02d}' for i in range(1, 32) ]

#data = 'chlc'
data = 'wind'

if data == 'chlc':
    for year in years:
        for month in months:
            get_chlc_data(year, month)
elif data == 'wind':
    for year in years:
        for month in months:
            for day in days:
                get_wind_data(year, month, day)
