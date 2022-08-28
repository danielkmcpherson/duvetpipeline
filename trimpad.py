import numpy as np
from astropy.io import fits
import glob
import os
import shutil

gal_list = ['ugc1385_red', 'ugc1385_blue']

for gal in gal_list:
    print(gal)
    images = np.array([])
    for file in glob.glob(gal + '/*.fits'):
        images = np.append(images, file[-15:-12])
    images = list(set(images))
    images.sort()
    location = gal
    img = glob.glob(gal + '/*.fits')[1][-26:-15]
    print(img)
    imglist = ('icubed', 'icubes', 'vcubes')
    print('Trimming Padding')
    for exptype in imglist:
        for num in images:
            cube1fname = location + '/' + img + str(num) + '_' + exptype + '.fits'
            cube1newfname = location + '/trimmed/' + img + str(num) + '_' + exptype + '_trimmed.fits'
            cube1 = fits.open(cube1fname)
            wstart = int((cube1[0].header['WAVGOOD0'] - cube1[0].header['CRVAL3']) / cube1[0].header['CD3_3'])
            wend = int((cube1[0].header['WAVGOOD1'] - cube1[0].header['CRVAL3']) / cube1[0].header['CD3_3'])
            ydim = len(cube1[0].data[1, :, 1])
            xdim = len(cube1[0].data[1, 1, :])
            cube1[0].data = cube1[0].data[wstart:wend, cube1[0].header['DARPADY']:(ydim - cube1[0].header['DARPADY']),
                            cube1[0].header['DARPADX']:(xdim - cube1[0].header['DARPADX'])]
            cube1[0].header['CRVAL3'] = cube1[0].header['CRVAL3'] + (cube1[0].header['CD3_3'] * wstart)
            cube1[0].header['CRPIX1'] = cube1[0].header['CRPIX1'] - cube1[0].header['DARPADX']
            cube1[0].header['CRPIX2'] = cube1[0].header['CRPIX2'] - cube1[0].header['DARPADY']
            cube1.writeto(cube1newfname, overwrite=True)
