from astropy.io import fits
import numpy as np
import glob
import os

types = ['mosaic', 'varcube', 'metacube']

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

for gal in gal_list:
    print(gal[0].split("_")[0])
    for exptype in types:
        try:
            os.remove('Reductions_Final/' + gal[0].split("_")[0] + '/' + gal[0] + '_' + exptype + '.fits')
            os.rename('Reductions_Final/' + gal[0].split("_")[0] + '/' + gal[0] + '_' + exptype + '_final.fits',
                      'Reductions_Final/' + gal[0].split("_")[0] + '/' + gal[0] + '_' + exptype + '.fits')

        except FileNotFoundError:

            print('No', exptype)