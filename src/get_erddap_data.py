import wget
from datetime import datetime
import os

def descargar_archivo(url, directory):
    try:
        print(url)
        wget.download(url, directory)
        print("\nDescarga completada.")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        
def get_SST_data(year, month):
    '''
    Source: 
    '''
    url = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdHadISST.nc?sst%5B(2018-01-16T12:00:00Z):1:(2018-04-16T12:00:00Z)%5D%5B(89.5):1:(-89.5)%5D%5B(-179.5):1:(179.5)%5D'
    print(url)

def get_chlc_data(year, month):
    '''
    Source: 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.graph?chlor_a'
    '''
    src = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.nc?chlor_a'
    url = f'{src}%5B({year}-{month}-01T12:00:00Z)%5D%5B(0.0)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Cchlor_a&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    print(url)
    directory = f'chlc/{year}/'
    os.makedirs(directory, exist_ok=True)
    descargar_archivo(url, directory)

min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110

years = [2014, 2015, 2016, 2017, 2018]
months = [f'{i:02d}' for i in range(1, 13) ]

for year in years:
    for month in months:
        get_chlc_data(year, month)

