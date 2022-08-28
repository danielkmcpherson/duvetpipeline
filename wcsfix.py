from astropy.io import fits
import numpy as np
import glob
import os

types = ['icubes', 'icubed', 'vcubes']

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

for gal in gal_list:
    for type in types:
        print(gal[0])
        images = np.array([])
        for file in glob.glob(gal[0] + '/trimmed/*trimmed.fits'):
            images = np.append(images, file[-23:-20])
        images = list(set(images))
        images.sort()
        location = gal[0]
        img = glob.glob(gal[0] + '/trimmed/*trimmed.fits')[1][-34:-23]

        cube0 = fits.open(gal[0] + '/trimmed/' + img + images[0] + '_' + type + '_trimmed.fits')
        hdr0 = cube0[0].header
        cube0.close()

        for num in images:

            cube = fits.open(gal[0] + '/trimmed/' + img + num + '_' + type + '_trimmed.fits')
            cube[0].header['CRPIX1'] = hdr0['CRPIX1']
            cube[0].header['CRPIX2'] = hdr0['CRPIX2']
            cube[0].header['CRVAL1'] = hdr0['CRVAL1']
            cube[0].header['CRVAL2'] = hdr0['CRVAL2']
            cube[0].header['CD1_1'] = hdr0['CD1_1']
            cube[0].header['CD1_2'] = hdr0['CD1_2']
            cube[0].header['CD2_1'] = hdr0['CD2_1']
            cube[0].header['CD2_2'] = hdr0['CD2_2']

            cube.writeto(gal[0] + '/trimmed/' + img + num + '_' + type + '_trimmed2.fits', overwrite=True)
            cube.close()
