from MontagePy.main import *
from astropy.io import fits
import glob

types = [('icubes', 'mosaic'), ('icubed', 'dosaic'), ('vcubes', 'varcube')]

gal_list = [('J131603_red', 0), ('KISSR1578_red', 0), ('ngc1569_pointing_1_red', -0.0003),
            ('ngc1569_pointing_2_red', -0.0003), ('ngc1569_pointing_3_red', -0.0003)]

for gal in gal_list:
    for exptype in types:
        print(gal[0])
        hdrcube = glob.glob(gal[0] + '/short/' + exptype[0] + '/*_aligned.fits')[1]
        print('Creating Table')
        rtn = mImgtbl(gal[0] + '/short/' + exptype[0], gal[0] + '/short/' + exptype[0] + '/cubes_c1.tbl')
        print(rtn)
        print('Creating Header')
        cube1 = fits.open(hdrcube)
        hdr1 = cube1[0].header
        hdr1.totextfile(gal[0] + '/short/' + exptype[0] + '/cubes_c1.hdr', endcard=True)
        print('Adding Cubes')
        adding = mAddCube(gal[0] + '/short/' + exptype[0],
                          gal[0] + '/short/' + exptype[0] + '/cubes_c1.tbl',
                          gal[0] + '/short/' + exptype[0] + '/cubes_c1.hdr',
                          gal[0] + '/short/' + gal[0] + '_' + exptype[1] + '_short.fits')
        print(adding)
        print('Finished, my dude!')