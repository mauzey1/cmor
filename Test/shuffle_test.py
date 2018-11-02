import cmor
import numpy
import time
import csv
import os

log_name = 'shuffle_test.log'


def write_cmor_file(nlat, nlon, nlev, ntimes, data, shuffle, deflate, deflate_level):
    dlat = 180. / nlat
    dlon = 360. / nlon
    dlev = 1000. / nlev

    lats = numpy.arange(-90 + dlat / 2., 90, dlat)
    blats = numpy.arange(-90, 90 + dlat, dlat)
    lons = numpy.arange(0 + dlon / 2., 360., dlon)
    blons = numpy.arange(0, 360. + dlon, dlon)

    levs = numpy.array([1000., 925, 900, 850, 800, 700, 600, 500, 400, 300,
                        250, 200, 150, 100, 75, 70, 50, 30, 20, 10, 7.5, 5, 2.5, 1, .5, .1])

    cmor.setup(inpath='Tables', netcdf_file_action=cmor.CMOR_REPLACE, logfile=log_name)
    cmor.dataset_json("Test/common_user_input.json")
    table = 'CMIP6_Amon.json'
    cmor.load_table(table)

    ilat = cmor.axis(
        table_entry='latitude',
        coord_vals=lats,
        cell_bounds=blats,
        units='degrees_north')
    ilon = cmor.axis(
        table_entry='longitude',
        coord_vals=lons,
        cell_bounds=blons,
        units='degrees_east')
    itim = cmor.axis(table_entry='time', units='months since 2010')
    ilev = cmor.axis(table_entry='plev19', coord_vals=levs, units='hPa')

    axes = [itim, ilev, ilat, ilon]

    var = cmor.variable(table_entry='ta', units='K', axis_ids=axes)

    cmor.set_deflate(var, shuffle, deflate, deflate_level)

    for i in range(ntimes):
        cmor.write(var, data[i,:,:,:], time_vals=numpy.array([float(i), ]), time_bnds=numpy.array([i, i + 1.]))

    filename = cmor.close(var_id=var, file_name=True)
    cmor.close()
    os.remove(log_name)

    return filename


defSet = [
            {'shuffle': 0, 'deflate': 1, 'deflate_level': 1},
            {'shuffle': 1, 'deflate': 1, 'deflate_level': 1}
        ]
nTimes = [1, 2, 5, 10]
dLat = 360
dLon = 720
iters = 20
saveFiles = True

with open('shuffle_test.csv', 'w') as csvfile:
    fieldnames = ['shuffle', 'deflate', 'deflate_level', 'nLat', 'nLon', 'nTimes', 'fileSize', 'time', 'iteration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for nt in nTimes:
        nLat = dLat
        nLon = dLon
        nLev = 26
        for it in range(iters):
            data = numpy.random.random((nt, nLev, nLat, nLon)) * 30 + 273.15
            for ds in defSet:
                t = time.time()
                filename = write_cmor_file(nLat, nLon, nLev, nt, data, ds['shuffle'], ds['deflate'], ds['deflate_level'])
                t = time.time() - t
                stats = os.stat(filename)
                row = {'nLat': nLat, 'nLon': nLon, 'nTimes': nt, 'fileSize': stats.st_size, 'time': t, 'iteration': it}
                row.update(ds)
                writer.writerow(row)
                print('{iteration}: shuffle = {shuffle}, deflate = {deflate}, deflate_level = {deflate_level}, nLat = {nLat}, nLon = {nLon}, nTimes = {nTimes}, size = {fileSize} bytes, time = {time}'.format(**row))
                if saveFiles:
                    basename = os.path.basename(filename)
                    path = os.path.join(os.getcwd(), 'shuffle_test', 's%s_d%s_l%s'%(ds['shuffle'], ds['deflate'], ds['deflate_level']))
                    path = os.path.join(path, '%dx%dx%d'%(nLat,nLon,nt))
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    newFilename = os.path.join(path, '.'.join([basename,'%d'%(it)]))
                    os.rename(filename,newFilename)
                else:
                    os.remove(filename)