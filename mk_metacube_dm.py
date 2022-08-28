import numpy as np
from matplotlib.pylab import *
from astropy.io import fits
from astropy import wcs
from scipy import interpolate
import glob

# Note that qfitsview crop and save does not alter the header, so the
# crop needs to be done here.
#
# These bounds seem good for this setting so can be applied
# universally when this setting/configuration is used
#
# Also note that python counts from 0, fits from 1. I determined the
# crop values from qfitsview

types = [('icubes', 'mosaic'), ('icubed', 'dosaic'), ('vcubes', 'varcube')]

gal_list = [('J131603_red', 0.037), ('KISSR1578_red', 0.02795), ('ngc1569_pointing_1_red', -0.0003),
            ('ngc1569_pointing_2_red', -0.0003), ('ngc1569_pointing_3_red', -0.0003)]

for gal in gal_list:
    for exptype in types:

        print(gal[0])
        images = np.array([])
        for file in glob.glob(gal[0] + '/long/*' + exptype[0] + '_aligned.fits'):
            images = np.append(images, file[-23:-20])
        images = list(set(images))
        images.sort()
        location = gal[0]
        img = glob.glob(gal[0] + '/long/*' + exptype[0] + '_aligned.fits')[1][-34:-23]

        dimcube = fits.open(gal[0] + '/long/' + img + images[0] + '_' + exptype[0] + '_aligned.fits')
        dimdata = dimcube[0].data
        dimhdr = dimcube[0].header

        shape = np.shape(dimdata)
        lamstart = dimhdr['CRVAL3']
        deltalam = dimhdr['CD3_3']
        lamlength = dimhdr['NAXIS3']

        z = 1 + gal[1]
        hgammalambda = 4340.471
        hbetalambda = 4861.333
        oiii4959lambda = 4958.911
        oiii5007lambda = 5006.843

        hgammashift = hgammalambda * z
        hgammaexpwindowcent = int(round((hgammashift - lamstart) / deltalam, 0))
        hgammawindowleft = hgammaexpwindowcent - 20
        
        hbetashift = hbetalambda * z
        hbetaexpwindowcent = int(round((hbetashift - lamstart) / deltalam, 0))
        hbetawindowleft = hbetaexpwindowcent - 20
        
        oiii4959shift = oiii4959lambda * z
        oiii4959expwindowcent = int(round((oiii4959shift - lamstart) / deltalam, 0))
        oiii4959windowleft = oiii4959expwindowcent - 20
        
        oiii5007shift = oiii5007lambda * z
        oiii5007expwindowcent = int(round((oiii5007shift - lamstart) / deltalam, 0))
        oiii5007windowleft = oiii5007expwindowcent - 20

        for num in images:
            xlen = [0, shape[1]]
            ylen = [0, shape[2]]
        
            xpix = np.arange(xlen[0], xlen[1], 1)
            ypix = np.arange(ylen[0], ylen[1], 1)

            # ==============================================================================
            # CREATE SATURATION MASKS FOR EACH EXPOSURE USING ICUBED FILES (counts)
        
            # Read in each cube for the four different exposure times (1200s: 81,
            # 600s: 82, 300s: 83, 100s: 86) with the red setting: Large BM 4780Ang
        
            cubed1 = fits.open(gal[0] + '/long/' + img + num + '_icubed_aligned.fits')
            icubed1 = cubed1[0].data
            ihdrd1 = cubed1[0].header
        
            # Set wavelength array -- assuming the ranges are the same for each
            # cube (seems fine)
        
            lamstart = ihdrd1['CRVAL3']
            deltalam = ihdrd1['CD3_3']
            lamlength = ihdrd1['NAXIS3']
            wavegood = [ihdrd1['WAVGOOD0'], ihdrd1['WAVGOOD1']]
            waver = np.arange(wavegood[0], wavegood[1] - deltalam, deltalam)
        
            waverloi = int((wavegood[0] - lamstart) / deltalam)
            waverhii = int((wavegood[1] - lamstart) / deltalam)
        
            # Set saturation level in the counts
            # Saturation seems to occur at ~8800 counts
        
            fsat = 5500
            print(fsat)
        
            # print(len(waver),len(ypix),len(xpix))
        
            mask1 = np.zeros((len(waver) + 1, len(xpix) + 1, len(ypix) + 1))
            linemask = np.ones((1,40), int)
        
            # For each spaxel within the xcrop and ycrop bounds:
            for ispaxval in xpix:
                for jspaxval in ypix:
        
                    count = 0
                    # For each wavelength
                    for fcounts in icubed1[waverloi:waverhii, ispaxval, jspaxval]:
        
                        # Check that the data are not saturated
                        if fcounts < fsat and mask1[count, ispaxval - xpix[0], jspaxval - ypix[0]] != 1:
                            # This is a good pixel, keep it
        
                            mask1[count, ispaxval - xpix[0], jspaxval - ypix[0]] = 0
        
                        elif fcounts >= fsat:
                            # This is a bad pixel, mask it out
        
                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0]] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0]] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0]] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0]] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0]] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0]] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] + 1] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0]] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0]] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0]] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0], jspaxval - ypix[0] - 1] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] + 1] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] + 1, jspaxval - ypix[0] - 1] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] + 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] + 1] = linemask

                            mask1[hbetawindowleft:hbetawindowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii4959windowleft:oiii4959windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] - 1] = linemask
                            mask1[oiii5007windowleft:oiii5007windowleft + 40, ispaxval - xpix[0] - 1, jspaxval - ypix[0] - 1] = linemask

                        count += 1
        
            mask_hdu = fits.PrimaryHDU(mask1, ihdrd1)
            mask_hdu.writeto(gal[0] + '/mask/' + img + num + '_mask.fits', overwrite=True)
            # ==============================================================================
            # NORMALIZE THE SPECTRA TO ONE EXPOSURE
        
            # Read in each cube for the four different exposure times (1200s: 81,
            # 600s: 82, 300s: 83, 100s: 86) with the red setting: Large BM 4800Ang
        
            cubes1 = fits.open(gal[0] + '/long/' + img + num + '_' + exptype[0] + '_aligned.fits')
            icubes1 = cubes1[0].data
            ihdrs1 = cubes1[0].header
        
            cubes2 = fits.open(gal[0] + '/short/' + gal[0] + '_' + exptype[1] + '_short.fits')
            icubes2 = cubes2[0].data
            ihdrs2 = cubes2[0].header
            
            # Set wavelength arrays for each cube - they should be the same, but
            # set each just in case
            #
            # These arrays are purely so I know which regions to average
            # over. Fits files record things in a different way.
        
            lamstart1 = ihdrs1['CRVAL3']
            deltalam1 = ihdrs1['CD3_3']
            lamlength1 = ihdrs1['NAXIS3']
            wavegood1 = [ihdrs1['WAVGOOD0'], ihdrs1['WAVGOOD1']]
            wave1 = np.arange(lamstart1, lamstart1 + (lamlength1 * deltalam1), deltalam1)
        
            lamstart2 = ihdrs2['CRVAL3']
            deltalam2 = ihdrs2['CD3_3']
            lamlength2 = ihdrs2['NAXIS3']
            wavegood2 = [ihdrs2['WAVGOOD0'], ihdrs2['WAVGOOD1']]
            wave2 = np.arange(lamstart2, lamstart2 + (lamlength2 * deltalam2), deltalam2)
        
            # Ignore the spectrum within these wavelength bounds:
            # These are the emission lines Hgamma, Hbeta, OIII doublet
        
            emislines = [[int(hgammashift) - 20, int(hgammashift) + 20], [int(hbetashift) - 20, int(hbetashift) + 20],
                         [int(oiii4959shift) - 20, int(oiii4959shift) + 20], [int(oiii5007shift) - 20, int(oiii5007shift) + 20]]
        
            # Create wavelength bins over which to average the continuum
            # Yeah, it's ugly. Whatevs
            wavedelta = 50.0
            if wavegood1[0] == wavegood2[0] and wavegood1[1] == wavegood2[1]:
                wavebins = [[wavegood1[0], emislines[0][0]],
                            [emislines[0][1], emislines[0][1] + (1 * wavedelta)],
                            [emislines[0][1] + (1 * wavedelta), emislines[0][1] + (2 * wavedelta)],
                            [emislines[0][1] + (2 * wavedelta), emislines[0][1] + (3 * wavedelta)],
                            [emislines[0][1] + (3 * wavedelta), emislines[0][1] + (4 * wavedelta)],
                            [emislines[0][1] + (4 * wavedelta), emislines[0][1] + (5 * wavedelta)],
                            [emislines[0][1] + (5 * wavedelta), emislines[0][1] + (6 * wavedelta)],
                            [emislines[0][1] + (6 * wavedelta), emislines[0][1] + (7 * wavedelta)],
                            [emislines[0][1] + (7 * wavedelta), emislines[0][1] + (8 * wavedelta)],
                            [emislines[0][1] + (8 * wavedelta), emislines[0][1] + (9 * wavedelta)],
                            [emislines[0][1] + (9 * wavedelta), emislines[1][0]],
                            [emislines[1][1], emislines[2][0]],
                            [emislines[2][1], emislines[3][0]],
                            [emislines[3][1], emislines[3][1] + (1 * wavedelta)],
                            [emislines[3][1] + (1 * wavedelta), wavegood1[1]]]
        
                wavebinsc = np.zeros([len(wavebins)])
                for i in range(len(wavebins)):
                    wavebinsc[i] = (wavebins[i][0] + wavebins[i][1]) / 2.0
            # print(wavebinsc)
        
            else:
                print('The good wavelengths are not equal across exposures!')
        
            cubes = [icubes1, icubes2]
        
            metacube = np.zeros((len(waver), len(xpix), len(ypix)))
            
            # For each spaxel within the xcrop and ycrop bounds:
            for ispaxval in xpix:
                for jspaxval in ypix:
        
                    # For each exposure:
                    expsplines = []
                    expmeansall = []
                    for exp in range(len(cubes)):
        
                        # Find the mean value in each wavelength bin
                        expmeans = np.zeros([len(wavebinsc)])
                        for wbin in range(len(wavebins)):
                            waveloindex = int((wavebins[wbin][0] - lamstart1) / deltalam1)
                            wavehiindex = int((wavebins[wbin][1] - lamstart1) / deltalam1)
                            meancont = np.mean(cubes[exp][waveloindex:wavehiindex + 1, \
                                               ispaxval, jspaxval])
        
                            expmeans[wbin] = meancont
        
                        # print(wavebins[wbin][0],wavebins[wbin][1],meancont)
        
                        expmeansall.append(expmeans)
        
                        # Fit the mean(wavelength) functions (spline?)
                        espline = interpolate.interp1d(wavebinsc, expmeans,
                                                       kind='quadratic',
                                                       fill_value='extrapolate')
        
                        xnew = np.arange(wavegood1[0], wavegood1[1], deltalam1)
                        expsplines.append(espline(xnew))
        
                    # Determine the offsets(wavelength) for each exp compared to
                    # 600s/82
                    #
                    # The 1200s/81 exposure is too saturated across the entire
                    # spectrum in a few pixels so comparison is bad
                    offset11 = expsplines[0] - expsplines[0]
                    offset12 = expsplines[0] - expsplines[1]
        
                    offsets = np.array([offset11, offset12])
        
                    # Apply the offsets(wavelength)
                    # For each exposure
                    cubefix = []
                    for exp in [0, 1]:
                        waveloindex = int((wavegood1[0] - lamstart1) / deltalam1)
                        wavehiindex = int((wavegood1[1] - lamstart1) / deltalam1)
                        cubeflux = cubes[exp][waveloindex:wavehiindex + 1,
                                   ispaxval, jspaxval]
        
                        cubeflux += offsets[exp]
        
                        cubefix.append(cubeflux)
        
                    # xnew = np.arange(wavegood6[0],wavegood6[1],deltalam6)
        
                    # -----------
                    # Apply saturation masks and average spectra
        
                    # for each wavelength
                    for wavelength in waver:
                        # take the average of exposures for which the pixels are
                        # not saturated
        
                        waveindex = int((wavelength - wavegood[0]) / deltalam)
        
                        m1 = mask1[waveindex, ispaxval - xpix[0], jspaxval - ypix[0]]
        
                        if m1 == 0:
                            finalflux = cubefix[0][waveindex]
        
                        else:
                            finalflux = cubefix[1][waveindex]
                            
                        metacube[waveindex,ispaxval - xpix[0],jspaxval - ypix[0]] = finalflux
                        
            # Save to file - tricky, have to think in fits format
            # Flux in every pixel (x,y,z)
        
            metacube_hdu = fits.PrimaryHDU(metacube, ihdrs1)
            mhdu = metacube_hdu.header
            mhdu['CRVAL3'] = wavegood[0]
            mhdu['NAXIS3'] = len(waver)
            mhdu['CRPIX1'] = ihdrd1['CRPIX1']
            mhdu['CRPIX2'] = ihdrd1['CRPIX2']
        
            metacube_hdu.writeto(gal[0] + '/replaced/' + exptype[0] + '/' + img + num + '_' + exptype[0] + '_replaced.fits', overwrite=True)
