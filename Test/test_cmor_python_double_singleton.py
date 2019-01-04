import common
import cmor
import os
import unittest
import base_test_cmor_python


class TestCase(base_test_cmor_python.BaseCmorTest):

    def testDoubleSingleton(self):
        try:
            cmor.setup(inpath=self.testdir,
                    netcdf_file_action=cmor.CMOR_REPLACE,
                    logfile=self.logfile)

            cmor.dataset_json(os.path.join(self.testdir, "CMOR_input_example.json"))
            cmor.load_table(os.path.join(self.tabledir, 'CMIP6_6hrLev.json'))
            itim, ilat, ilon = common.read_cmor_time_lat_lon()

            ilambda = cmor.axis(
                table_entry='lambda550nm',
                units='m',
                length=1,
                coord_vals=[550.,],
                cell_bounds=[500.,600.])
            # Creates two singleton dims?

            varid = cmor.variable(table_entry=common.specs["BS"]["entry"],
                                units=common.specs["BS"]["units"],
                                axis_ids=[itim, ilat, ilon, ilambda],
                                missing_value=1.e28,
                                positive=common.specs["BS"]["positive"],
                                original_name="BS")
            for index in range(2):
                tim_array, bnds_tim = common.read_time(index)
                data = common.read_2d_input_files(index, "BS", (common.lat, common.lon))
                print data.shape, data
                print tim_array, bnds_tim
                cmor.write(var_id=varid, data=data, ntimes_passed=1,
                        time_vals=tim_array, time_bnds=bnds_tim)
                print("Passed write")
            cmor.close()
            self.processLog()
        except BaseException:
            raise


if __name__ == '__main__':
    unittest.main()