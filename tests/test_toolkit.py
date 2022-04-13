import pandas as pd
import os
import sys
from pandas.testing import assert_frame_equal
import unittest

sys.path.append('../src/injury_severity_toolkit')

from src.injury_severity_toolkit import CCI_Calculator, SOFA_Calculator, APACHEIII_Calculator, VFDs


class TestToolkit(unittest.TestCase):
    def test_cci(self):
        qc = pd.read_csv("expected/CCI_QC.csv")
        CCI_Calculator.run(pd.read_csv("./test_src/CCI_Test_src.csv"), True)
        results = pd.read_csv("CCI_test.csv")
        assert_frame_equal(qc, results)
        os.unlink("CCI_test.csv")

    def test_sofa(self):
        qc = pd.read_csv("expected/SOFA_QC.csv")
        SOFA_Calculator.run(pd.read_csv("./test_src/SOFA_test_src_final.csv"), True)
        results = pd.read_csv("SOFA_test.csv")
        assert_frame_equal(qc, results, check_dtype=False)
        os.unlink("SOFA_test.csv")

    def test_VFDs(self):
        qc = pd.read_csv("expected/VFDs_QC.csv")
        VFDs.run(pd.read_csv("./test_src/VFDs_test_src.csv"), True)
        results = pd.read_csv("VFDs_test.csv")
        assert_frame_equal(qc, results)
        os.unlink("VFDs_test.csv")

    def test_APACHE(self):
        qc = pd.read_csv("expected/APACHE_QC.csv")
        APACHEIII_Calculator.run(pd.read_csv("./test_src/APACHE_test_src.csv"), True)
        results = pd.read_csv("APACHE_test.csv")
        assert_frame_equal(qc, results, check_dtype=False)
        os.unlink("APACHE_test.csv")
