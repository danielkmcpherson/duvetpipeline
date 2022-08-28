from astropy.io import fits
import numpy as np
import glob

types = ['mosaic', 'varcube', 'metacube']

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

for gal in gal_list:
    print(gal[0].split("_")[0])
    for exptype in types:
        try:
            cube = fits.open('Reductions_Final/' + gal[0].split("_")[0] + '/' + gal[0] + '_' + exptype + '.fits')
            cube[0].header['BUNIT'] = ('FLAM16', 'b units (*10^{-16} erg cm^{-2} s^{-1} A^{-1})')
            del cube[0].header['CD1_1']
            del cube[0].header['CD1_2']
            del cube[0].header['CD2_1']
            del cube[0].header['CD2_2']
            del cube[0].header['CD3_3']
            cube.writeto('Reductions_Final/' + gal[0].split("_")[0] + '/' + gal[0] + '_' + exptype + '_final.fits', overwrite=True)

        except FileNotFoundError:

            print('No', exptype)

        except KeyError:

            print('Some header value doesnt exist')