import cmor
import numpy
import os
import unittest
import base_test_cmor_python


class TestCase(base_test_cmor_python.BaseCmorTest):

    def testJoergTim2Clim02(self):
        try:
            cmor.setup(inpath=self.tabledir,
                    netcdf_file_action=cmor.CMOR_REPLACE_3, 
                    logfile=self.logfile)
            cmor.dataset_json(os.path.join(self.testdir, "common_user_input.json"))

            table = 'CMIP6_Oclim.json'
            cmor.load_table(table)
            axes = [{'table_entry': 'time2',
                    'units': 'days since 1850-01-01 00:00:00',
                    'coord_vals': [15.5, 45, ],
                    'cell_bounds':[[0, 31], [31, 62]]
                    },
                    {'table_entry': 'depth_coord',
                    'units': 'm',
                    'coord_vals': [5000., 3000., 2000., 1000.],
                    'cell_bounds': [5000., 3000., 2000., 1000., 0]},
                    {'table_entry': 'latitude',
                    'units': 'degrees_north',
                    'coord_vals': [0],
                    'cell_bounds': [-1, 1]},
                    {'table_entry': 'longitude',
                    'units': 'degrees_east',
                    'coord_vals': [90],
                    'cell_bounds': [89, 91]},
                    ]

            axis_ids = list()
            for axis in axes:
                print 'doing:', axis
                axis_id = cmor.axis(**axis)
                axis_ids.append(axis_id)

            for var, units, value in (('difvso', 'm2 s-1', 274.),):
                values = numpy.ones(map(lambda x: len(x["coord_vals"]), axes)) * value
                values = values.astype("f")
                varid = cmor.variable(var,
                                    units,
                                    axis_ids,
                                    history='variable history',
                                    missing_value=-99
                                    )
                cmor.write(varid, values)

            cmor.close()
            self.processLog()
        except BaseException:
            raise


if __name__ == '__main__':
    unittest.main()