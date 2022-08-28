from astropy.io import fits
import numpy as np
imglist = ('mosaic', 'varcube')
gal = 'ugc1385'

for type in imglist:

	cube1 = fits.open('C:/Users/salkv/Desktop/Reductions/' + gal + '_red/combined/' + gal + '_red_' + type + '.fits')
	cube1[0].data = cube1[0].data[:, 0:103, 2:69]
	cube1[0].header['CRPIX1'] = cube1[0].header['CRPIX1'] - 2
	cube1[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube1[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube1[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube1.writeto('C:/Users/salkv/Desktop/Reductions/Reductions_Final/' + gal + '/' + gal + '_red_' + type + '.fits')

	cube2 = fits.open('C:/Users/salkv/Desktop/Reductions/' + gal + '_blue/combined/' + gal + '_blue_' + type + '.fits')
	cube2[0].data = cube2[0].data[:, 0:103, 3:70]
	cube2[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube2[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube2[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube2[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube2.writeto('C:/Users/salkv/Desktop/Reductions/Reductions_Final/' + gal + '/' + gal + '_blue_' + type + '.fits')
