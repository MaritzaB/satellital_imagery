import wget
from datetime import datetime

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
    url = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41mday.nc?sst%5B({year}-{month}-16T00:00:00Z)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Csst&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    descargar_archivo(url, 'sst')
    
min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110

year = '2019'
month = '01'

def get_CHL_data(year, month):
    '''
    Source:
    - 2014: Chlorophyll, NOAA S-NPP VIIRS, Science Quality, Global 4km, Level 3, 2012-present, Monthly 
    - 2015-2018: Chlorophyll a, North Pacific, NOAA VIIRS, 750m resolution, 2015-present (Monthly Composite)
    '''
    # url = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisVHNSQchlaMonthly.graph?chlor_a%5B(2014-01-01T12:00:00Z)%5D%5B(0.0)%5D%5B(54.99375):(23.006249999999994)%5D%5B(-162.99374999999998):(-110.00625)%5D&.draw=surface&.vars=longitude%7Clatitude%7Cchlor_a&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    url = f'https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMBchla1day.nc?chlor_a%5B({year}-{month}-16T12:00:00Z)%5D%5B({min_lat}):({max_lat})%5D%5B({min_lon}):({max_lon})%5D&.draw=surface&.vars=longitude%7Clatitude%7Cchlor_a&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff'
    descargar_archivo(url, 'chl')
    
def get_wind_speed_data(year, month):
    '''
    Source:
    - FNMOC 10m Surface Winds, 360x181, Monthly
    '''
    #PENDIENTE

