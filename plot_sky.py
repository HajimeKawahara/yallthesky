
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

# plotting 
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='aitoff')

# Convert RA and Dec to SkyCoord
coords = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame='icrs')
ycoords = SkyCoord(ra=yra * u.deg, dec=ydec * u.deg, frame='icrs')

# Plot stars on the map
#ax.scatter(coords.ra.wrap_at(180 * u.deg).radian, coords.dec.radian, marker='o', s=0.3, c='blue', label='Stars',alpha=0.05)
ax.scatter(coords.ra.wrap_at(180 * u.deg).radian, coords.dec.radian, marker='o', s=1, c='blue', label='Stars',alpha=0.1)

# Plot Y-dwarfs on the map
ax.scatter(ycoords.ra.wrap_at(180 * u.deg).radian, ycoords.dec.radian, marker='o', s=20, c='purple', label='known Y-dwarfs',alpha=0.7)

# Customize the plot
ax.grid(True)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_xticklabels(['4h', '3h', '0h', '21h', '20h'])
ax.set_xlabel('RA')
ax.set_ylabel('Dec')
ax.legend()

# Show the plot
plt.title('Sky Projection Map with Stars within '+str(dpc)+' pc')
plt.grid(True)
plt.savefig("stars"+str(dpc)+"pc.png")
plt.show()
