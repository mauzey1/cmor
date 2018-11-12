import cmor
import numpy
import time
import csv
import os
import netCDF4

log_name = 'shuffle_test_missing_data.log'
nc_file = 'dpco2_Omon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gn_185001-199912.nc'

def write_cmor_file(lat, lon, ntimes, data, dmask, shuffle, deflate, deflate_level):
    
    cmor.setup(inpath='Tables', netcdf_file_action=cmor.CMOR_REPLACE, logfile=log_name)
    cmor.dataset_json("Test/common_user_input.json")
    
    cmor_table_obj = cmor.load_table("CMIP6_grids.json")

    # create x-y axes
    ix = cmor.axis(
        table_entry='x',
        units='m',
        coord_vals=numpy.arange(mask.shape[0]))
    iy = cmor.axis(
        table_entry='y',
        units='m',
        coord_vals=numpy.arange(mask.shape[1]))

    # create latitude-longitude grid
    grid_id = cmor.grid(
        axis_ids=[
            ix,
            iy],
        latitude=lat,
        longitude=lon)

    cmor.load_table('CMIP6_Omon.json')
    itim = cmor.axis(table_entry='time', units='months since 2010')

    axes = [itim, grid_id]

    var = cmor.variable(table_entry='dpco2', units='Pa', axis_ids=axes)

    cmor.set_deflate(var, shuffle, deflate, deflate_level)

    # write time slices of data to file while applying mask
    for i in range(ntimes):
        masked = numpy.ma.MaskedArray(data[i,:,:], dmask, fill_value=1e20)
        cmor.write(var, masked, time_vals=numpy.array([float(i), ]), time_bnds=numpy.array([i, i + 1.]))

    filename = cmor.close(var_id=var, file_name=True)
    cmor.close()
    os.remove(log_name)

    return filename


# get lat-lon and mask from NetCDF file
with netCDF4.Dataset(nc_file, 'r', format='NETCDF4') as nc_root:
    mask = nc_root.variables['dpco2'][0,:,:].mask
    lat = nc_root.variables['nav_lat'][:]
    lon = nc_root.variables['nav_lon'][:]

defSet = [
            {'shuffle': 0, 'deflate': 1, 'deflate_level': 1},
            {'shuffle': 1, 'deflate': 1, 'deflate_level': 1}
        ]
nTimes = [1, 2, 5, 10, 20, 50, 100]
# nTimes = [1000, 2000, 5000, 10000, 20000]
# nTimes = [50000]
dLat = mask.shape[0]
dLon = mask.shape[1]
iters = 50
saveFiles = True

statsList = []
for nt in nTimes:
    nLat = dLat
    nLon = dLon
    for it in range(iters):
        data = numpy.random.random((nt, nLat, nLon)) * 30 + 273.15
        for ds in defSet:
            # create file
            t = time.time()
            filename = write_cmor_file(lat, lon, nt, data, mask, ds['shuffle'], ds['deflate'], ds['deflate_level'])
            t = time.time() - t

            # get file size
            stats = os.stat(filename)
            row = {'nLat': nLat, 'nLon': nLon, 'nTimes': nt, 'fileSize': stats.st_size, 'time': t, 'iteration': it}
            row.update(ds)
            statsList.append(row)
            print('{iteration}: shuffle = {shuffle}, deflate = {deflate}, deflate_level = {deflate_level}, nLat = {nLat}, nLon = {nLon}, nTimes = {nTimes}, size = {fileSize} bytes, time = {time}'.format(**row))

            # Save output file to a results directory.  Otherwise, delete file.
            if saveFiles:
                basename = os.path.basename(filename)
                path = os.path.join(os.getcwd(), 'shuffle_test_missing_data', 's%s_d%s_l%s'%(ds['shuffle'], ds['deflate'], ds['deflate_level']))
                path = os.path.join(path, '%dx%dx%d'%(nLat,nLon,nt))
                if not os.path.isdir(path):
                    os.makedirs(path)
                newFilename = os.path.join(path, '.'.join([basename,'%d'%(it)]))
                os.rename(filename,newFilename)
            else:
                os.remove(filename)

# write statistics to CSV file
with open('shuffle_test_missing_data.csv', 'w') as csvfile:
    fieldnames = ['shuffle', 'deflate', 'deflate_level', 'nLat', 'nLon', 'nTimes', 'fileSize', 'time', 'iteration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in statsList:
        writer.writerow(r)
