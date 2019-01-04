import cmor
import os
import unittest
import base_test_cmor_python


class TestCase(base_test_cmor_python.BaseCmorTest):

    def test1DVar(self):
        try:
            cmor.setup(inpath=self.tabledir, netcdf_file_action=cmor.CMOR_REPLACE, logfile=self.logfile)

            cmor.dataset_json(os.path.join(self.testdir, "CMOR_input_example.json"))

            cmor.load_table("CMIP6_Omon.json")
            itim = cmor.axis(
                table_entry='time',
                units='months since 2010-1-1',
                coord_vals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                cell_bounds=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

            ivar = cmor.variable('thetaoga', units='deg_C', axis_ids=[itim, ])

            data = [280., ] * 12  # 12 months worth of data

            cmor.write(ivar, data)

            cmor.close()

            self.processLog()
        except BaseException:
            raise


if __name__ == '__main__':
    unittest.main()