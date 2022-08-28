from astropy.io import fits
import numpy as np
import glob

gal_list = [('ugc1385_red', 6), ('ugc1385_blue', 6)]

for gal in gal_list:
    print(gal[0])
    cube = fits.open(gal[0] + '/combined/' + gal[0] + '_varcube.fits')
    cube[0].data = cube[0].data/ (gal[1] * (1.35/0.29))
    cube.writeto(gal[0] + '/combined/' + gal[0] + '_varcube_2.fits', overwrite=True)