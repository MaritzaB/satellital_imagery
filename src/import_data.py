from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np

temperature = loadmat('data/datos/chla_mat/2015_sst_mountly.mat')
y = loadmat('data/datos/chla_mat/latitud.mat')
x = loadmat('data/datos/chla_mat/longitud.mat')

temp_m1 = temperature['CompSST'][:,:,0]
lat = y['varlat'][:,:]
lon = x['varlon'][:,:]

# Filtrado de datos
temp_m1[temp_m1>33] = np.nan
temp_m1[temp_m1<21] = np.nan

print(np.nanmax(temp_m1[0]), np.nanmin(temp_m1))
plt.pcolor(lon, lat, temp_m1)
plt.xlabel('Longitude (degrees west)')
plt.ylabel('Latitude (degrees north)')
plt.grid()
plt.title('Promedio mensual de la temperatura')
plt.colorbar()
plt.clim(25,30)
plt.savefig('plt.png')
