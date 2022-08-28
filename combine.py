from MontagePy.main import *
from astropy.io import fits
import glob

types = [('icubes', 'mosaic'), ('icubed', 'dosaic'), ('vcubes', 'varcube')]

gal_list = [('ugc1385_red', 0.018749166), ('ugc1385_blue', 0.018749166)]

for gal in gal_list:
    for exptype in types:
        print(gal[0])
        hdrcube = glob.glob(gal[0] + '/reprojected/' + exptype[0] + '/*.fits')[1]
        print(hdrcube)
        print('Creating Table')
        rtn = mImgtbl(gal[0] + '/reprojected/' + exptype[0], gal[0] + '/reprojected/' + exptype[0] + '/cubes_c1.tbl')
        print(rtn)
        print('Creating Header')
        cube1 = fits.open(hdrcube)
        hdr1 = cube1[0].header
        hdr1.totextfile(gal[0] + '/reprojected/' + exptype[0] + '/cubes_c1.hdr', endcard=True)
        print('Adding Cubes')
        adding = mAddCube(gal[0] + '/reprojected/' + exptype[0],
                          gal[0] + '/reprojected/' + exptype[0] + '/cubes_c1.tbl',
                          gal[0] + '/reprojected/' + exptype[0] + '/cubes_c1.hdr',
                          gal[0] + '/combined/' + gal[0] + '_' + exptype[1] + '.fits')
        print(adding)
        print('Finished, my dude!')
