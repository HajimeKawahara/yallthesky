import numpy as np
import healpy as hp
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table



#db="GAIA"
db="TICv8"

if db == "TICv8":
    # read TIC v8 within 200 pc this csv is computed in allthesky directory in whaleshark
    try:
        dat = pd.read_csv("ticv8_200pc.csv")
    except:
        print("download from https://secondearths.sakura.ne.jp/ticv8_200pc.csv")
        exit()
    plx = dat["plx"]
elif db == "GAIA":
    #read gaia 100pc
    dat = pd.read_csv("gaia100pc.csv", delimiter=",")
    plx = dat["parallax"]

plt.hist(1000.0/plx,bins=100)
x=np.logspace(0.5,np.log10(200.),100)
n10expect = 200. #Nstar at 10pc expected
a=n10expect/100.0
plt.plot(x,a*x**2, ls="dashed", label="$\propto d^2$")
plt.yscale("log")
plt.xscale("log")
plt.xlabel("distance (pc)")
plt.ylabel("# of stars")
plt.legend()
plt.savefig("ddepend.png")
plt.show()   
#count within 10/20 pc
dpc10 = 20
plxcrit10=1000.0/dpc10
datlim10 = dat[plx>plxcrit10]
n10 = len(datlim10)
print(n10)
    
dpc = 200
plxcrit=1000.0/dpc
datlim = dat[plx>plxcrit]
n = len(datlim)
print(n)

ra = datlim["ra"].values
dec = datlim["dec"].values

#read known Y-dwarfs
ydat = pd.read_csv("ultracoolbd_ydwarf.csv")
yra=ydat["R.A. (deg)"]
ydec=ydat["Decl. (deg)"]


#density
nside=8
npix = hp.nside2npix(nside)
fac=np.pi/180.0
print(np.max(dec*fac+np.pi/2.0), np.min(dec*fac+np.pi/2.0))
pixdat = hp.ang2pix(nside, np.pi/2.0 - dec*fac,ra*fac)
fov = 1/40.0
density = np.bincount(pixdat)*npix*fov/n10

mean = np.nanmean(density)
hp.visufunc.mollview(density, coord="E", min=np.min(density),max=np.min(density)*2)#, flip="geo")

plt.savefig("density"+db+str(dpc)+"pc.png")
plt.show()
