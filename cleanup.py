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
        for file in glob.glob(gal + '_red' + '/trimmed/*trimmed.fits'):
            images = np.append(images, file[-23:-20])
        images = list(set(images))
        images.sort()
        img = glob.glob(gal + '_red' + '/trimmed/*trimmed.fits')[1][-34:-23]

        for num in images:
            os.remove(gal + '_red' + '/trimmed/' + img + num + '_' + type + '_trimmed.fits')
            os.rename(gal + '_red' + '/trimmed/' + img + num + '_' + type + '_trimmed2.fits', gal + '_red' + '/trimmed/' + img + num + '_' + type + '_trimmed.fits')

for gal in gal_list:
    for type in types:
        print(gal)
        images = np.array([])
        for file in glob.glob(gal + '_blue' + '/trimmed/*trimmed.fits'):
            images = np.append(images, file[-23:-20])
        images = list(set(images))
        img = glob.glob(gal + '_blue' + '/trimmed/*trimmed.fits')[1][-34:-23]

        for num in images:
            os.remove(gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed.fits')
            os.remove(gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed2.fits')
            os.rename(gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed3.fits', gal + '_blue' + '/trimmed/' + img + num + '_' + type + '_trimmed.fits')