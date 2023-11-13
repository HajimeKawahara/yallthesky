import numpy as np
import healpy as hp
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table

db="GAIA"
if db == "TICv8":
    # read TIC v8 within 200 pc this csv is computed in allthesky directory in whaleshark 
    dat = pd.read_csv("ticv8_200pc.csv")
elif db == "GAIA":
    #read gaia 100pc
    dat = pd.read_csv("gaia100pc.csv", delimiter=",")
    
dpc = 100
plxcrit=1000.0/dpc
if db == "TICv8":
    datlim = dat[dat["plx"]>plxcrit]
elif db == "GAIA":
    datlim = dat[dat["parallax"]>plxcrit]

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
pixdat = hp.ang2pix(nside, np.pi/2.0 - dec*fac,ra*fac)
density = np.bincount(pixdat)/np.sum(ra)
mean = np.nanmean(density)
hp.visufunc.mollview(density/mean, coord="E", min=np.min(density)/mean,max=np.min(density)*3/mean)#, flip="geo")

plt.savefig("density"+db+str(dpc)+"pc.png")
plt.show()
