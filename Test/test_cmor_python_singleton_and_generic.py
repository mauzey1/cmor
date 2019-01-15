#!/usr/bin/env python

import cmor
import numpy


def main():

    cmor.setup(inpath='Tables',
               netcdf_file_action=cmor.CMOR_REPLACE)
    cmor.dataset_json("Test/CMOR_input_example.json")

    table = 'CMIP6_6hrLev.json'
    cmor.load_table(table)
    axes = [{'table_entry': 'time1',
             'units': 'days since 2000-01-01 00:00:00'},
            {'table_entry': 'latitude',
             'units': 'degrees_north',
             'coord_vals': [0],
             'cell_bounds': [-1, 1]},
            {'table_entry': 'longitude',
             'units': 'degrees_east',
             'coord_vals': [90],
             'cell_bounds': [89, 91]},
            {'table_entry': 'hybrid_height',
             'coord_vals': [0, 1],
             'cell_bounds': [[0., 0.5], [0.5, 1.]],
             'units': 'm'},
            {'table_entry': 'lambda550nm',
             'coord_vals': [550.,],
             'cell_bounds': [500.,600.],
             'units': 'm'}
            ]

    values = numpy.array([1.2, 1.2], numpy.float32)
    numpy.reshape(values, (2, 1, 1, 1))
    axis_ids = list()
    for axis in axes:
        axis_id = cmor.axis(**axis)
        axis_ids.append(axis_id)

    cmor.zfactor(axis_ids[3], 'b', '', axis_ids[3:4],
                 'd', [0., 0.5], [[0., 0.25], [0.25, 1.]])
    cmor.zfactor(axis_ids[3], 'orog', 'm', axis_ids[1:3], 'd', [[0.]])
    print 'cmor.zfactor calls complete'
    varid = cmor.variable('ec550aer',
                          'm-1',
                          axis_ids,
                          missing_value=-99
                          )

    cmor.write(varid, values, time_vals=[6.0], time_bnds=[3., 12.])
    cmor.close()


if __name__ == '__main__':

    main()
