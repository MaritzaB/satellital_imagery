from netCDF4 import Dataset
import matplotlib.pyplot as plt
import glob # extraer archivos de diferente extension

filename = 'data/datos/sst_nc/SST_20200111.nc'
data = Dataset(filename, mode='r')
temperature = data['analysed_sst'][0][:,:]
lon = data['longitude'][:]
lat = data['latitude'][:]

plt.pcolor(lon,lat,temperature)
plt.xlabel('Longitude (degrees west)')
plt.ylabel('Latitude (degrees north)')
plt.grid()
plt.title('Promedio mensual de la temperatura')
plt.colorbar()
plt.savefig('images/antartida_temp.png')

datafiles = glob.glob('data/datos-2607/*.nc')
#print(datafiles[1])
#print(Dataset(datafiles[1])

file20190101 = Dataset(datafiles[1])
sla = file20190101['sla'][0][:,:]
lon2 = file20190101['longitude'][:]-360
lat2 = file20190101['latitude'][:]

plt.pcolor(lon2,lat2,sla)
plt.title('SLA global')
plt.savefig('images/global_sla.png')
print(file20190101.variables.keys())
print(file20190101.variables["sla"])
#print(sla[1])
