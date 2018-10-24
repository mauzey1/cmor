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
cmor.load_table("Tables/CMIP6_6hrPlevPt.json")
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
plev27 = numpy.array([100000, 97500, 95000, 92500, 90000, 87500, 85000, 82500, 80000, 
                      77500, 75000, 70000, 65000, 60000, 55000, 50000, 45000, 40000, 
                      35000, 30000, 25000, 22500, 20000, 17500, 15000, 12500, 10000])

plev7h = numpy.array([92500, 85000, 70000, 60000, 50000, 25000, 5000])

itim = cmor.axis(
    table_entry='time1',
    units='months since 2030-1-1',
    length=ntimes,
    interval='1 month')

ilev27 = cmor.axis(
    table_entry='plev27',
    units='Pa',
    coord_vals=plev27,
    cell_bounds=None)

ilev7h = cmor.axis(
    table_entry='plev7h',
    units='Pa',
    coord_vals=plev7h,
    cell_bounds=None)


for it in range(ntimes):

    var_grplmxrat = cmor.variable(
        table_entry='grplmxrat27',
        units='1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev27, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='grplmxrat')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev27), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_grplmxrat,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_grplmxrat)

    var_rainmxrat = cmor.variable(
        table_entry='rainmxrat27',
        units='1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev27, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='rainmxrat')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev27), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_rainmxrat,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_rainmxrat)

    var_snowmxrat = cmor.variable(
        table_entry='snowmxrat27',
        units='1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev27, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='snowmxrat')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev27), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_snowmxrat,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_snowmxrat)

    var_cldicemxrat = cmor.variable(
        table_entry='cldicemxrat27',
        units='1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev27, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='cldicemxrat')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev27), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_cldicemxrat,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_cldicemxrat)

    var_cldwatmxrat = cmor.variable(
        table_entry='cldwatmxrat27',
        units='1',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev27, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='cldwatmxrat')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev27), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_cldwatmxrat,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_cldwatmxrat)

    var_wbptemp = cmor.variable(
        table_entry='wbptemp7h',
        units='K',
        comment='My wise comments here',
        axis_ids=numpy.array((ilev7h, ilon, ilat, itim)),
        missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
        original_name='wbptemp')

    time = numpy.array((it))
    bnds_time = numpy.array((it, it + 1))
    data3d = numpy.random.random((len(plev7h), nlon, nlat)) * 30. + 265.
    data3d = data3d.astype('f')
    error_flag = cmor.write(
        var_id=var_wbptemp,
        data=data3d,
        ntimes_passed=1,
        time_vals=time,
        time_bnds=bnds_time)

    cmor.close(var_wbptemp)


error_flag = cmor.close()
