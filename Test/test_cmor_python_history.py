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
import os
import unittest
import base_test_cmor_python
import sys
import tempfile
import cdms2
import time


class TestCase(base_test_cmor_python.BaseCmorTest):

    def testCMIP6_historytemplate(self):
        # -------------------------------------------
        # Try to call cmor with a bad institution_ID
        # -------------------------------------------
        try:
            cmor.setup(inpath=self.tabledir, netcdf_file_action=cmor.CMOR_REPLACE, logfile=self.logfile)
            cmor.dataset_json(os.path.join(self.testdir, "CMOR_input_example.json"))
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
                type=numpy.dtype('float32').char,
                units='kg')

            data = numpy.random.random(5).astype('float32')
            # set fill_value
            data[0]=23;
            data[4]=23;

            cmor.set_cur_dataset_attribute("_history_template", "%s; CMOR mip_era is: <mip_era>")
            cmor.set_cur_dataset_attribute("history", "myMIP")
            for i in range(0, 5): 
                cmor.write(ivar, data[i:i])
            cmor.close()
            self.processLog()
        except BaseException:
            raise

        version =time.strftime("%Y%m%d")
        f=cdms2.open("CMIP6/CMIP6/ISMIP6/PCMDI/PCMDI-test-1-0/piControl-withism/r3i1p1f1/Omon/masso/gn/v"+version+"/masso_Omon_PCMDI-test-1-0_piControl-withism_r3i1p1f1_gn_201001-201005.nc")
        history=f.history
        self.assertIn("CMOR mip_era is: CMIP6",history)
        self.assertIn("myMIP",history)



if __name__ == '__main__':
    unittest.main()