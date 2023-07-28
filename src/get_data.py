import wget
from datetime import datetime
from bs4 import BeautifulSoup

def date_2_nday(date_str):
    date_object = datetime.strptime(date_str, "%Y%m%d")
    n_day = date_object.timetuple().tm_yday
    n_day_3digits = "{:03d}".format(n_day)
    return n_day_3digits

print(date_2_nday('20140101'))

def get_url(year, month, day):
    folder = 'data'
    processing_level = 'L4'
    fecha = f'{year}{"{:02d}".format(month)}{"{:02d}".format(day)}'
    temperature_type = 'ghrsst'
    sst_type = 'MUR25'
    scale = 'GLOB'
    institution = 'JPL'
    day = date_2_nday(fecha)
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


url, folder= get_url(2014,11,1)

print(url, folder)

descargar_archivo(url, folder)
