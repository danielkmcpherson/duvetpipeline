from astropy.io import fits
import numpy as np
import glob
import os

types = ['icubes', 'icubed', 'vcubes']

gal_list = ['ugc1385']

for gal in gal_list:
    for type in types:
        print(gal)
        images = np.array([])
        for file in glob.glob(gal + '_blue' + '/trimmed/*trimmed2.fits'):
            images = np.append(images, file[-24:-21])
        images = list(set(images))
        images.sort()
        img = glob.glob(gal + '_blue' + '/trimmed/*trimmed2.fits')[1][-35:-24]
        redimg = glob.glob(gal + '_red' + '/trimmed/*trimmed2.fits')[1][-35:-24]
        rednum = glob.glob(gal + '_red' + '/trimmed/*trimmed2.fits')[1][-24:-21]

        cube0 = fits.open(gal + '_red' + '/trimmed/' + redimg + rednum + '_' + type + '_trimmed2.fits')
        hdr0 = cube0[0].header
        cube0.close()

        for num in images:

            cube = fits.open(gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed2.fits')
            cube[0].header['CRPIX1'] = hdr0['CRPIX1']
            cube[0].header['CRPIX2'] = hdr0['CRPIX2']
            cube[0].header['CRVAL1'] = hdr0['CRVAL1']
            cube[0].header['CRVAL2'] = hdr0['CRVAL2']
            cube[0].header['CD1_1'] = hdr0['CD1_1']
            cube[0].header['CD1_2'] = hdr0['CD1_2']
            cube[0].header['CD2_1'] = hdr0['CD2_1']
            cube[0].header['CD2_2'] = hdr0['CD2_2']

            cube.writeto(gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed3.fits', overwrite=True)
            cube.close()
