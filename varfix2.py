from astropy.io import fits
import numpy as np
import glob

from astropy.io import fits
import numpy as np
import glob

gal_list = [('J131603_red', 3, 6), ('KISSR1578_red', 3, 8)]

for gal in gal_list:
    print(gal[0])
    images = np.array([])
    for file in glob.glob(gal[0] + '/replaced/vcubes/*.fits'):
        images = np.append(images, file[-17:-14])
    images = list(set(images))
    images.sort()
    img = glob.glob(gal[0] + '/replaced/vcubes/*.fits')[1][-28:-17]
    for num in images:
        cube1 = fits.open(gal[0] + '/replaced/vcubes/' + img + str(num) + '_replaced.fits')
        data = cube1[0].data
        hdr = cube1[0].header
        cube2 = fits.open(gal[0] + '/mask/' + img + str(num) + '_mask.fits')
        mask = cube2[0].data
        shape = np.shape(data)
        specpix = np.arange(0, shape[0], 1)
        xpix = np.arange(0, shape[1], 1)
        ypix = np.arange(0, shape[2], 1)
        for i in xpix:
            for j in ypix:
                for k in specpix:
                    if mask[k, i, j] == 1:
                        data[k, i, j] = data[k, i, j] / (gal[1] * (1.35/0.29))
                    else:
                        data[k, i, j] = data[k, i, j] / (gal[2] * (1.35/0.29))
        fixcube = fits.PrimaryHDU(data, hdr)
        fixcube.writeto(gal[0] + '/replaced/vcubes/' + img + str(num) + '_replaced_2.fits')