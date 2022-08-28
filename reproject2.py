import numpy as np
from astropy.io import fits
from MontagePy.main import *
import glob

types = ['icubes', 'icubed', 'vcubes']

gal_list = [('J131603_red', 0.037), ('KISSR1578_red', 0.02795), ('ngc1569_pointing_1_red', -0.0003),
            ('ngc1569_pointing_2_red', -0.0003), ('ngc1569_pointing_3_red', -0.0003)]

for gal in gal_list:
    for exptype in types:
        print(gal[0])
        images = np.array([])
        for file in glob.glob(gal[0] + '/replaced/' + exptype + '/*.fits'):
            images = np.append(images, file[-17:-14])
        images = list(set(images))
        images.sort()
        location = gal[0]
        img = glob.glob(gal[0] + '/replaced/' + exptype + '/*.fits')[1][-28:-17]

        dims = fits.open(gal[0] + '/replaced/' + exptype + '/' + img + images[0] + '_replaced.fits')
        dimshdr = dims[0].header
        arearatio = dimshdr['PXSCL'] / dimshdr['SLSCL']
        print(arearatio)

        print('Creating Table')
        rtn = mImgtbl(gal[0] + '/replaced/' + exptype, gal[0] + '/replaced/' + exptype + '/cubes_c1.tbl')
        print('Creating Header')
        rtn2 = mMakeHdr(gal[0] + '/replaced/' + exptype + '/cubes_c1.tbl', gal[0] + '/replaced/' + exptype + '/cubes_c1.hdr')

        print('Reprojecting Cubes')

        for num in images:
            proj1 = mProjectCube(gal[0] + '/replaced/' + exptype + '/' + img + num + '_replaced.fits',
                                 gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected.fits',
                                 gal[0] + '/replaced/' + exptype + '/cubes_c1.hdr', drizzle=1.0, energyMode=False, fluxScale=arearatio)
            print(proj1)

        print('Fixing Headers')

        origcube = fits.open(gal[0] + '/replaced/' + exptype + '/' + img + num + '_replaced.fits')
        orighdr = origcube[0].header

        for num in images:
            projcube = fits.open(gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected.fits')
            projhdr = projcube[0].header
            orighdr['BITPIX'] = projhdr.get('BITPIX')
            orighdr['NAXIS'] = projhdr.get('NAXIS')
            orighdr['NAXIS1'] = projhdr.get('NAXIS1')
            orighdr['NAXIS2'] = projhdr.get('NAXIS2')
            orighdr['NAXIS3'] = projhdr.get('NAXIS3')
            orighdr['CTYPE1'] = projhdr.get('CTYPE1')
            orighdr['CTYPE2'] = projhdr.get('CTYPE2')
            orighdr['EQUINOX'] = projhdr.get('EQUINOX')
            orighdr['CRVAL1'] = projhdr.get('CRVAL1')
            orighdr['CRVAL2'] = projhdr.get('CRVAL2')
            orighdr['CRVAL3'] = projhdr.get('CRVAL3')
            orighdr['CRPIX1'] = projhdr.get('CRPIX1')
            orighdr['CRPIX2'] = projhdr.get('CRPIX2')
            orighdr['CRPIX3'] = projhdr.get('CRPIX3')
            orighdr['CDELT1'] = projhdr.get('CDELT1')
            orighdr['CDELT2'] = projhdr.get('CDELT2')
            orighdr['CDELT3'] = orighdr.get('CD3_3')
            orighdr['CROTA2'] = projhdr.get('CROTA2')
            projcube[0].header = orighdr
            projcube.writeto(
                gal[0] + '/reprojected/' + exptype + '/' + img + num + '_' + exptype + '_reprojected_hdrfix.fits')