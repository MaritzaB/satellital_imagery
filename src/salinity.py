from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

datafile = 'data/salinidad/4903185_prof.nc'
data = Dataset(datafile, mode='r')
#print(data.variables.keys())

temperature = data['TEMP'][:][0,:]
salinity = data['PSAL'][:][0,:]
pressure = data['PRES'][:][0,:]

plt.plot(temperature, salinity, '+')
plt.xlabel('Temperature (degrees Celsius)')
plt.ylabel('Salinity (gkg-1)')
plt.savefig('images/temperatures_vs_salinity.png')

plt.figure(2)
plt.hist(temperature)
plt.savefig('images/temperature_histogram.png')

# Anomalía espacial estandarizada AEE
def aee(x):
    aee = (x - np.nanmean(x) / np.std(x))
    return aee

ztemperature = aee(temperature)
zsalinity = aee(salinity)

plt.figure(3)
plt.plot(ztemperature, zsalinity, '+')
plt.xlabel('Temperature (degrees Celsius)')
plt.ylabel('Salinity (gkg-1)')
plt.savefig('images/temperatures_vs_salinity_anomaly.png')
