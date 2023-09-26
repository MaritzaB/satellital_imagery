import wget
from datetime import datetime
from bs4 import BeautifulSoup

# https://www.ncei.noaa.gov/data/oceans/ghrsst/L4/
#

def date_2_nday(date_str):
    date_object = datetime.strptime(date_str, "%Y%m%d")
    n_day = date_object.timetuple().tm_yday
    n_day_3digits = "{:03d}".format(n_day)
    return n_day_3digits

def julian_2_date(year, julian_day):
    date_object = datetime.strptime(f'{year} {julian_day}', '%Y %j')
    return date_object.strftime('%Y%m%d')

def get_url_noaa(year, julian_day):
    folder = 'data'
    processing_level = 'L4'
    fecha = julian_2_date(year, julian_day)
    temperature_type = 'ghrsst'
    sst_type = 'MUR25'
    scale = 'GLOB'
    institution = 'JPL'
    day = julian_day
    filename = f'{fecha}090000-JPL-L4_GHRSST-SSTfnd-MUR-{scale}-v02.0-fv04.1.nc'
    src = f'https://www.ncei.noaa.gov/data/oceans'
    url = f'{src}/{temperature_type}/{processing_level}/{scale}/{institution}/{sst_type}/{year}/{day}/{filename}'
    directory = f'{folder}/{filename}'
    return url, directory

def descargar_archivo(url, directory):
    try:
        print(url)
        wget.download(url, directory)
        print("\nDescarga completada.")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        
years = [2014, 2015, 2016, 2017,]
julian_days = [ f'{i:03d}' for i in range(1, 121) ]

for year in years:
    for julian_day in julian_days:
        url, folder = get_url_noaa(year, julian_day)
        descargar_archivo(url, folder)
