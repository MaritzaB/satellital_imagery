from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import glob
import numpy as np
from numpy import linalg as la

datafile = 'data/salinidad/4903185_prof.nc'
data = Dataset(datafile, mode='r')
#print(data.variables.keys())

temperature = data['TEMP'][:][0,:]
salinity = data['PSAL'][:][0,:]
pressure = data['PRES'][:][0,:]

# Escalar los datos
scaler = MinMaxScaler()
#scaled_temperature = scaler.fit(temperature)
#scaled_salinity = scaler.fit(temperature)
matrix = np.array([temperature, salinity]).T
scaled_matrix = scaler.fit_transform(matrix)
print(np.shape(scaled_matrix))

plt.figure(1)
plt.plot(temperature, salinity)
plt.xlabel('temperature')
plt.ylabel('salinity')
plt.title('Datos sin escalar de temperatura vs salinidad')
plt.savefig('images/scaled_temp_vs_sal.png')

# Clustering
clustering = KMeans(n_clusters=4, init = 'random', max_iter=300, n_init=10).fit(scaled_matrix)
cluster = clustering.labels_
clustering_matrix = np.array([temperature, salinity, cluster]).T

print(clustering.inertia_ (i for i in range(1,5)))

centroid, label = KMeans.cluster_centers_, KMeans.labels_