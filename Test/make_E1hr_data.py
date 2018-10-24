import cmor
import numpy

error_flag = cmor.setup(inpath='Test', netcdf_file_action=cmor.CMOR_REPLACE)

error_flag = cmor.dataset_json("Test/common_user_input.json")

# creates 10 degree grid
nlat = 18
nlon = 36
alats = numpy.arange(180) - 89.5
bnds_lat = numpy.arange(181) - 90.
alons = numpy.arange(360) + .5
bnds_lon = numpy.arange(361)
cmor.load_table("Tables/CMIP6_E1hr.json")
ilat = cmor.axis(
    table_entry='latitude',
    units='degrees_north',
    length=nlat,
    coord_vals=alats,
    cell_bounds=bnds_lat)

ilon = cmor.axis(
    table_entry='longitude',
    length=nlon,
    units='degrees_east',
    coord_vals=alons,
    cell_bounds=bnds_lon)

ntimes = 1
plevs = numpy.array([100000, 97500, 95000, 92500, 90000, 87500, 85000, 82500, 80000, 
                     77500, 75000, 70000, 65000, 60000, 55000, 50000, 45000, 40000, 
                     35000, 30000, 25000, 22500, 20000, 17500, 15000, 12500, 10000])


itim = cmor.axis(
    table_entry='time1',
    units='months since 2030-1-1',
    length=ntimes,
    interval='1 month')

ilev = cmor.axis(
    table_entry='plev27',
    units='Pa',
    coord_vals=plevs,
    cell_bounds=None)


for it in range(ntimes):

    var_tntr = cmor.variable(
        table_entry='tntr27',
        units='K s-1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='tntr')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_tntr,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_tntr)

    var_zg = cmor.variable(
        table_entry='zg27',
        units='m',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='zg')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_zg,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_zg)

    var_utendnogw = cmor.variable(
        table_entry='utendnogw27',
        units='m s-2',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='utendnogw')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_utendnogw,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_utendnogw)

    var_vtendnogw = cmor.variable(
        table_entry='vtendnogw27',
        units='m s-2',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='vtendnogw')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_vtendnogw,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_vtendnogw)


error_flag = cmor.close()
