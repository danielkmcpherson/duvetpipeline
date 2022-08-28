from astropy.io import fits
import numpy as np
import glob

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

trims = np.arange(0,4,1)

for gal in gal_list:
    print(gal[0])
    images = np.array([])
    for file in glob.glob(gal[0] + '/hgamma/*.fits'):
        images = np.append(images, file[-17:-14])
    images = list(set(images))
    images.sort()
    location = gal[0]
    img = glob.glob(gal[0] + '/hgamma/*.fits')[1][-28:-17]

    cube0 = fits.open(gal[0] + '/hgamma/' + img + images[0] + '_hgamma_0.fits')
    data0 = cube0[0].data
    hdr0 = cube0[0].header

    aligns = np.zeros([len(images[1:]) * 20, 5])

    for num in images[1:]:

        a = images[1:].index(num)
        print(num)
        xshift = np.arange(-2, 3, 1)
        yshift = np.arange(-2, 3, 1)
        chisq = np.zeros([len(trims), len(xshift), len(yshift)])

        for trim in trims:

            cube = fits.open(gal[0] + '/hgamma/' + img + num + '_hgamma_' + str(trim) + '.fits')
            data = cube[0].data
            hdr = cube[0].header
            clipx = 6
            clipy = 2

            shape = np.shape(data)

            for x in xshift:
                for y in yshift:

                    window1 = data0[clipx:shape[0] - clipx, clipy:shape[1] - clipy]
                    window2 = data[(clipx + x):(shape[0] - clipx + x), (clipy + y):(shape[1] - clipy + y)]
                    diff = np.abs(window1) - np.abs(window2)
                    diffsq = np.square(diff)
                    div = np.divide(diffsq, np.abs(window1))
                    chi = np.sum(div)
                    # print('Trim:', trim, 'Spaxel:', x, y, 'Chi:', chi)
                    chisq[trim, x + 2, y + 2] = chi

        for b in np.arange(0,20,1):
            minind = np.unravel_index(np.argmin(chisq), chisq.shape)
            align = (minind[0], minind[1] - 2, minind[2] - 2)
            aligns[a * 20 + b, :] = (num, minind[0], minind[1] - 2, minind[2] - 2, chisq[minind])
            chisq[minind] = 1000000

    aligns = np.asarray(aligns)

    np.savetxt(gal[0] + '/aligns.csv', aligns, fmt='%s, %i, %i, %i, %f', delimiter=',')
