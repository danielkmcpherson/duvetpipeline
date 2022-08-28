from astropy.io import fits
import numpy as np
img = 'kb191020_00'
imglist = ('icubed', 'icubes', 'vcubes')

for type in imglist:

	cube1 = fits.open('resample/' + img + '104_' + type + '_resampled_0.fits')
	cube1[0].data = cube1[0].data[:, 0:70 , 0:23]
	cube1[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube1[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube1[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube1[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube1.writeto('aligned/' + img + '104_' + type + '_aligned.fits')

	cube2 = fits.open('resample/' + img + '105_' + type + '_resampled_0.fits')
	cube2[0].data = cube2[0].data[:, 0:70 , 0:23]
	cube2[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube2[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube2[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube2[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube2.writeto('aligned/' + img + '105_' + type + '_aligned.fits')
	
	cube3 = fits.open('resample/' + img + '106_' + type + '_resampled_0.fits')
	cube3[0].data = cube3[0].data[:, 0:70 , 0:23]
	cube3[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube3[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube3[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube3[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube3.writeto('aligned/' + img + '106_' + type + '_aligned.fits')
	
	cube4 = fits.open('resample/' + img + '107_' + type + '_resampled_0.fits')
	cube4[0].data = cube4[0].data[:, 0:70 , 0:23]
	cube4[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube4[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube4[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube4[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube4.writeto('aligned/' + img + '107_' + type + '_aligned.fits')
	
	cube5 = fits.open('resample/' + img + '108_' + type + '_resampled_0.fits')
	cube5[0].data = cube5[0].data[:, 0:70 , 0:23]
	cube5[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube5[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube5[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube5[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube5.writeto('aligned/' + img + '108_' + type + '_aligned.fits')
	
	cube6 = fits.open('resample/' + img + '109_' + type + '_resampled_0.fits')
	cube6[0].data = cube6[0].data[:, 0:70 , 0:23]
	cube6[0].header['CRPIX1'] = cube1[0].header['CRPIX1']
	cube6[0].header['CRPIX2'] = cube1[0].header['CRPIX2']
	cube6[0].header['CRVAL1'] = cube1[0].header['CRVAL1']
	cube6[0].header['CRVAL2'] = cube1[0].header['CRVAL2']
	cube6.writeto('aligned/' + img + '109_' + type + '_aligned.fits')
