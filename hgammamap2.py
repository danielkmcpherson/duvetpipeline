from astropy.io import fits
import numpy as np
from measureline import *
import glob

gal_list = [('J090704_red_1', 0.029), ('J090704_red_2', 0.029)]

for gal in gal_list:
    print(gal[0])
    cube = fits.open(gal[0] + '/combined/' + gal[0] + '_mosaic.fits')
    data = cube[0].data
    hdr = cube[0].header

    # Get some header info

    lamstart = hdr['CRVAL3']

    deltalam = hdr['CDELT3']
    lamlength = hdr['NAXIS3']

    # Redshift and Emission Line Wavelengths

    z = 1 + gal[1]
    hgammalambda = 4340.471
    hgammacontright = 4310

    # Find window positions of emission lines
    hgammashift = hgammalambda * z
    hgammaexpwindowcent = int(round((hgammashift - lamstart) / deltalam, 0))

    hgammacontrightshift = hgammacontright * z
    hgammacontrightwindow = int(round((hgammacontrightshift - lamstart) / deltalam, 0))

    # Last little bit of setup

    xpix = np.arange(0, np.shape(data)[1], 1)
    ypix = np.arange(0, np.shape(data)[2], 1)
    hgammaout = np.zeros([len(xpix), len(ypix)])

    # Ok fine, let's get to work.

    for i in xpix:
        for j in ypix:

            spec = data[:, i, j]

            # Dirty Continuum Calcs

            hgammacont = np.mean(spec[hgammacontrightwindow - 40:hgammacontrightwindow])

            # print(hgammacont)

            # hgamma

            try:

                hgammatruewindowleft, hgammatruewindowright, hgammatruewindowcent = dirtymeasure(
                    hgammaexpwindowcent, spec, hgammacont)

                hgammalinestrength = np.sum(spec[hgammatruewindowleft:hgammatruewindowright]) - hgammacont

            except IndexError:

                hgammalinestrength = 0

            # Write Line Strengths to Array

            hgammaout[i][j] = hgammalinestrength

    hgammacube = fits.PrimaryHDU(hgammaout, hdr)
    hgammacube.writeto(gal[0] + '/hgamma/' + gal[0] + '_hgamma.fits', overwrite=True)
