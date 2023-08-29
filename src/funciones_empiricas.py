# Funciones empíricas ortogonales FEOs.
# Cuando tenemos diferentes variables y queremos hacer un análisis de la
# relación entre ellas.

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import glob # extraer archivos de diferente extension
import numpy as np
from numpy import linalg as la

datafiles = glob.glob('data/datos/sst_gm/*.nc')

temperature_matrix = []
for i in range(0,len(datafiles)):
    temperature = Dataset(datafiles[i])['analysed_sst'][0].reshape(-1)
    temperature_matrix.append(temperature)
    del temperature

print(np.shape(temperature_matrix))

# Estandarización de la matriz
# Anomalía espacial estandarizada AEE
def aee(x):
    aee = (x - np.nanmean(x) / np.std(x))
    return aee

# Generación de matriz
a_vector = np.array(aee(temperature_matrix[0]),aee(temperature_matrix[1]))

#a = np.
# Matriz de covarianza
covariance_matrix = np.cov(a_vector)

# Cálculo de eigenvalores y eigenvectores
#v, d = la.eig(covariance_matrix)

#feos = a_vector * v

#first_feo = feos[0]

