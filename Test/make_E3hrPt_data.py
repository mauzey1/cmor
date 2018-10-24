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
cmor.load_table("Tables/CMIP6_E3hrPt.json")
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
plevs = numpy.array([92500, 85000, 70000, 60000, 50000, 25000, 5000])


itim = cmor.axis(
    table_entry='time1',
    units='months since 2030-1-1',
    length=ntimes,
    interval='1 month')

ilev = cmor.axis(
    table_entry='plev7h',
    units='Pa',
    coord_vals=plevs,
    cell_bounds=None)


for it in range(ntimes):

    var_ta = cmor.variable(
        table_entry='ta7h',
        units='K',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='ta')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_ta,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_ta)

    var_ua = cmor.variable(
        table_entry='ua7h',
        units='m s-1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='ua')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_ua,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_ua)

    var_va = cmor.variable(
        table_entry='va7h',
        units='m s-1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='va')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_va,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_va)

    var_wap = cmor.variable(
        table_entry='wap7h',
        units='Pa s-1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='wap')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_wap,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_wap)


error_flag = cmor.close()