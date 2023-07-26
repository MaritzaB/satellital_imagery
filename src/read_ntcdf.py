from netCDF4 import Dataset

filename = 'data/datos/sst_nc/SST_20200111.nc'
data = Dataset(filename, mode='r')
temperature = data['analysed_sst'][0][:,:]
lon = data['longitude'][:]
lat = data['latitude'][:]

print(lon, lat)
