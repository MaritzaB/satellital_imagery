import xarray as xr
import netCDF4 as nc
# Plot the data
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

nc_file = 'data/2014/01/2014_01_NESDIS_VHNSQ_chla.nc'
nc_data = nc.Dataset(nc_file)
print(nc_data.variables.keys())

sst_nc_file = 'data/2014/01/2014_01_jplMURSST41_.nc'
sst_nc_data = nc.Dataset(sst_nc_file)
print(sst_nc_data.variables.keys())

#file = 'data/2014/01/cmems_obs-wind_glo_phy_my_l4_P1M_201401_clipped.nc'
file = 'data/2014/01/2014_01_NESDIS_VHNSQ_chla.nc'

ds = xr.open_dataset(file)
#print('\n\n\nVariables with xarray :')
#print(ds.variables)
#daa = ds.drop_dims('altitude')
#print('\n\n\nVariables with xarray :')
#print(daa.variables)

print('\n\n\nChlora_variable:')
print(ds['chlor_a'].drop_vars('altitude'))


# plot the data with xarray

chla = ds['chlor_a']
chla.plot(norm=LogNorm(vmin=0.01, vmax=200), cmap='viridis')
plt.show()
plt.savefig('data/2014/01/chla.png')
