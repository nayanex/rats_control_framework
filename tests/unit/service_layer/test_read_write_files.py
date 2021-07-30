import filecmp
import shutil
import tempfile
from os import path

import pandas as pd

from src.automation.service_layer.read_write_files import (
    generate_dsv_file,
    generate_txt_file,
)
from tests.data.ey import AAHG

MOCK_TEXT = "The bug is on the table"


class TestReadWriteFiles:
    """
    Test Cases for reading and writing files, like text or dsv.
    """

    def setup_method(self):
        """
        Create testing scenario
        """
        self.test_dir = tempfile.mkdtemp()
        self.mock_txt_filename = path.join(self.test_dir, "mock.txt")
        self.mock_dsv_filename = path.join(self.test_dir, "mock.dsv")
        with open(self.mock_txt_filename, "w") as output_file:
            output_file.write(MOCK_TEXT)

    def teardown_method(self):
        """
        Tear down created scenario
        """
        shutil.rmtree(self.test_dir)

    def test_generate_dsv_file(self):
        """
        Test dsv file generation.
        """
        dsv_filename = path.join(self.test_dir, "file.dsv")
        generate_dsv_file(dsv_filename, AAHG, "|")
        mock_df = pd.read_csv(dsv_filename, sep="|", dtype=None)
        assert mock_df.columns.to_list().sort() == list(set(AAHG[0])).sort()

    def test_generate_txt_file(self):
        """
        Test generation of text file..
        """
        txt_filename = path.join(self.test_dir, "file.txt")
        generate_txt_file(txt_filename, MOCK_TEXT)
        assert filecmp.cmp(self.mock_txt_filename, txt_filename)
