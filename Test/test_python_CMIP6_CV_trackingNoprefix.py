# If this example is not executed from the directory containing the
# CMOR code, please first complete the following steps:
#
#   1. In any directory, create 'Tables/', 'Test/' and 'CMIP6/' directories.
#
#   2. Download
#      https://github.com/PCMDI/cmor/blob/master/TestTables/CMIP6_Omon.json
#      and https://github.com/PCMDI/cmor/blob/master/TestTables/CMIP6_CV.json
#      to the 'Tables/' directory.
#
#   3. Download
#      https://github.com/PCMDI/cmor/blob/master/Test/<filename>.json
#      to the 'Test/' directory.

import cmor
import numpy
import unittest
import sys
import os
import tempfile
import pkgutil
import netCDF4
import base_CMIP6_CV


# ==============================
#  main thread
# ==============================
def run():
    unittest.main()


class TestCase(base_CMIP6_CV.BaseCVsTest):

    def testCMIP6(self):
        # -------------------------------------------
        # Try to call cmor with a bad institution_ID
        # -------------------------------------------
        cmor.setup(inpath='Tables', netcdf_file_action=cmor.CMOR_REPLACE, logfile=self.tmpfile)
        cmor.dataset_json("Test/CMOR_input_example.json")

        # ------------------------------------------
        # load Omon table and create masso variable
        # ------------------------------------------
        cmor.load_table("CMIP6_Omon.json")
        itime = cmor.axis(table_entry="time", units='months since 2010',
                            coord_vals=numpy.array([0, 1, 2, 3, 4.]),
                            cell_bounds=numpy.array([0, 1, 2, 3, 4, 5.]))
        ivar = cmor.variable(
            table_entry="masso",
            axis_ids=[itime],
            units='kg')

        data = numpy.random.random(5)
        for i in range(0, 5):
            cmor.write(ivar, data[i:i])
        self.delete_files += [cmor.close(ivar, True)]
        filen = cmor.close()
        f = netCDF4.Dataset(cmor.get_final_filename(), "r")
        self.assertTrue("tracking_id" in f.__dict__)
        a = f.__dict__["tracking_id"].split('/')[0]
        self.assertNotIn("hdl:21.14100/", a)

    @unittest.skipIf(pkgutil.find_loader("cdms2") is None, "cdms2 not installed")
    def testCMIP6_CDMS2(self):
        import cdms2

        # -------------------------------------------
        # Try to call cmor with a bad institution_ID
        # -------------------------------------------
        cmor.setup(inpath='Tables', netcdf_file_action=cmor.CMOR_REPLACE, logfile=self.tmpfile)
        cmor.dataset_json("Test/CMOR_input_example.json")

        # ------------------------------------------
        # load Omon table and create masso variable
        # ------------------------------------------
        cmor.load_table("CMIP6_Omon.json")
        itime = cmor.axis(table_entry="time", units='months since 2010',
                            coord_vals=numpy.array([0, 1, 2, 3, 4.]),
                            cell_bounds=numpy.array([0, 1, 2, 3, 4, 5.]))
        ivar = cmor.variable(
            table_entry="masso",
            axis_ids=[itime],
            units='kg')

        data = numpy.random.random(5)
        for i in range(0, 5):
            cmor.write(ivar, data[i:i])
        self.delete_files += [cmor.close(ivar, True)]
        filen = cmor.close()
        f = cdms2.open(cmor.get_final_filename(), "r")
        a = f.getglobal("tracking_id").split('/')[0]
        self.assertNotIn("hdl:21.14100/", a)


if __name__ == '__main__':
    run()
