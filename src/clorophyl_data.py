import numpy as np
import matplotlib.pyplot as plt

filename = "data/datos/chla_py/chlorophyll"
x = "data/datos/chla_py/Lon"
y = "data/datos/chla_py/Lat"

var = np.load(filename, allow_pickle=True)
lon = np.load(x, allow_pickle=True)
lat = np.load(y, allow_pickle=True)

plt.pcolor(lon,lat,var)
plt.savefig('images/clorophyll.png')
