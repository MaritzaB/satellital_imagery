from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import glob

datafiles = glob.glob('data/datos/sst_gm/*.nc')
sst_file = Dataset(datafiles[0])
print(sst_file.variables.keys())

analysed_sst = sst_file['analysed_sst'][0][:,:]
lon = sst_file['longitude'][:]
lat = sst_file['latitude'][:]

plt.pcolor(lon,lat,analysed_sst)
plt.title('analysed_sst Golfo de México')
plt.savefig('images/analysed_sst_golfo.png')

# Extraer dato de un punto en específico

x1 = -94
y1 = 24


idx = np.where(lon == -94)
idy = np.where(lat == 24)

sample_station = analysed_sst[idx[0][0], idy[0][0]]

estacion = np.array(sample_station)
print(estacion)

# Promedio de matrices de los 9 archivos
variable_temperatura = []
for k in range(0,9):
    temp_diaria = sst_file['analysed_sst'][0]
    variable_temperatura.append(temp_diaria)
    del temp_diaria

variable_temperatura = np.array(variable_temperatura)

temperatura_promedio = np.mean(variable_temperatura[:,:,:], axis=0)
plt.pcolor(lon, lat, temperatura_promedio)
plt.title('Promedios de temperaturas diarias golfo')
plt.savefig('images/promedio_temperaturas.png')
