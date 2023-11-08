import numpy as np
import healpy as hp
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table

# read TIC v8 within 100 pc
dat = pd.read_csv("ticv8_100pc.csv")

dpc = 100
plxcrit=1000.0/dpc
datlim = dat[dat["plx"]>plxcrit]
ra = datlim["ra"].values
dec = datlim["dec"].values

#read known Y-dwarfs
ydat = pd.read_csv("ultracoolbd_ydwarf.csv")
yra=ydat["R.A. (deg)"]
ydec=ydat["Decl. (deg)"]


#density
nside=8
fac=np.pi/180.0
print(np.max(dec*fac+np.pi/2.0), np.min(dec*fac+np.pi/2.0))
pixdat = hp.ang2pix(nside, np.pi/2.0 - dec*fac,ra*fac+np.pi)
density = np.bincount(pixdat)/np.sum(ra)
hp.visufunc.mollview(density, coord="E", min=np.min(density),max=np.min(density)*2)

plt.savefig("density"+str(dpc)+"pc.png")
plt.show()
