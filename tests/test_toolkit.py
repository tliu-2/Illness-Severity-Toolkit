import pandas as pd
import os
import sys
from pandas.testing import assert_frame_equal
import unittest

sys.path.append('../src/injury_severity_toolkit')

from src.injury_severity_toolkit import CCI_Calculator


class TestCCI(unittest.TestCase):
    def test_cci(self):
        qc = pd.read_csv("expected/CCI_QC.csv")
        CCI_Calculator.run(pd.read_csv("./test_src/CCI_Test_src.csv"), True)
        results = pd.read_csv("CCI_Test.csv")
        assert_frame_equal(qc, results)
        os.unlink("CCI_Test.csv")

