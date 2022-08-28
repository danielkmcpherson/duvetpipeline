from astropy.io import fits
import numpy as np
import glob

types = ['icubes', 'icubed', 'vcubes']

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

trims = np.arange(0,4,1)

for gal in gal_list:
    for exptype in types:
        print(gal[0])
        images = np.array([])
        for file in glob.glob(gal[0] + '/trimmed/*trimmed.fits'):
            images = np.append(images, file[-23:-20])
        images = list(set(images))
        images.sort()
        location = gal[0]
        img = glob.glob(gal[0] + '/trimmed/*trimmed.fits')[1][-34:-23]

        for num in images:

            cube = fits.open(gal[0] + '/trimmed/' + img + num + '_' + exptype + '_trimmed.fits')
            data = cube[0].data
            hdr = cube[0].header

            shape = np.shape(data)
            resample = np.zeros((shape[0], shape[1], shape[2] * 4))

            xpix = np.arange(0, shape[1], 1)
            ypix = np.arange(0, shape[2], 1)

            # Ok fine, let's get to work.

            for i in xpix:
                for j in ypix:

                    resample[:, i, (j * 4)] = data[:, i, j] / 4
                    resample[:, i, (j * 4) + 1] = data[:, i, j] / 4
                    resample[:, i, (j * 4) + 2] = data[:, i, j] / 4
                    resample[:, i, (j * 4) + 3] = data[:, i, j] / 4

            shrink = np.zeros((shape[0], shape[1], shape[2] - 1))

            xpix2 = np.arange(0, shape[1], 1)
            ypix2 = np.arange(0, shape[2] - 1, 1)

            for trim in trims:
                for i in xpix2:
                    for j in ypix2:
                        shrink[:, i, j] = resample[:, i, ((j * 4) + trim)] + \
                                          resample[:, i, ((j * 4) + trim + 1)] + \
                                          resample[:, i, ((j * 4) + trim + 2)] + \
                                          resample[:, i, ((j * 4) + trim + 3)]

                resamplecube = fits.PrimaryHDU(shrink, hdr)
                resamplecube.writeto(gal[0] + '/resample/' + img + num + '_' + exptype + '_resampled_' + str(trim) + '.fits', overwrite=True)
