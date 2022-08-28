from astropy.io import fits
import numpy as np
import glob

gal_list = ['J090704']

for gal in gal_list:
    print(gal)

    cube0 = fits.open(gal + '_red_1/hgamma/' + gal + '_red_1_hgamma.fits')
    data0 = cube0[0].data
    hdr0 = cube0[0].header

    xshift = np.arange(-6, 7, 1)
    yshift = np.arange(-6, 7, 1)
    chisq = np.zeros([len(xshift), len(yshift)])

    cube = fits.open(gal + '_blue/hgamma/' + gal + '_blue_hgamma.fits')
    data = cube[0].data
    hdr = cube[0].header
    clipx = 10
    clipy = 10

    blueshape = np.shape(data)
    redshape = np.shape(data0)
    shape = [0, 0]
    print(redshape)
    print(blueshape)

    if redshape[0] < blueshape[0]:
        shape[0] = redshape[0]
    else:
        shape[0] = blueshape[0]

    if redshape[1] < blueshape[1]:
        shape[1] = redshape[1]
    else:
        shape[1] = blueshape[1]

    aligns = np.zeros([20, 3])

    for x in xshift:
        for y in yshift:

            window1 = data0[clipx:shape[0] - clipx, clipy:shape[1] - clipy]
            window2 = data[(clipx + x):(shape[0] - clipx + x), (clipy + y):(shape[1] - clipy + y)]
            diff = np.abs(window1) - np.abs(window2)
            diffsq = np.square(diff)
            div = np.divide(diffsq, np.abs(window1))
            chi = np.nansum(div)
            print(chi)
            # print('Trim:', trim, 'Spaxel:', x, y, 'Chi:', chi)
            chisq[x + 6, y + 6] = chi

    for b in np.arange(0,20,1):
        minind = np.unravel_index(np.argmin(chisq), chisq.shape)
        aligns[b, :] = (minind[0] - 6, minind[1] - 6, chisq[minind])
        chisq[minind] = 1000000

    aligns = np.asarray(aligns)

    np.savetxt(gal + '_blue' + '/aligns2.csv', aligns, fmt='%i, %i, %f', delimiter=',')
