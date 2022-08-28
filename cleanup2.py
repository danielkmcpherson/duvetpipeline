from astropy.io import fits
import numpy as np
import glob
import os

types = ['icubes', 'icubed', 'vcubes']

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

for gal in gal_list:
    for exptype in types:
        print(gal[0])
        images = np.array([])
        for file in glob.glob(gal[0] + '/reprojected/' + exptype + '/*_hdrfix.fits'):
            images = np.append(images, file[-34:-31])
        images = list(set(images))
        images.sort()
        print(images)
        location = gal[0]
        img = glob.glob(gal[0] + '/reprojected/' + exptype + '/*.fits')[1][-43:-32]
        print(img)

        for num in images:

            os.remove(gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected.fits')
            # os.remove(gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected_area.fits')
            os.rename(gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected_hdrfix.fits', gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected.fits')