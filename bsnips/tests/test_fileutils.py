import os
from unittest import TestCase
from bsnips.utils.fileutils import increment_file_number
from bsnips.utils.log import setup_logging

# setup_logging()


class TestFileUtils(TestCase):
    def setUp(self):
        pass

    def test_increment_file_number(self):
        filename = os.path.abspath(__file__)
        dir_path = os.path.dirname(filename)
        nf = increment_file_number(dir_path, filename)
        name, ext = os.path.splitext(filename)
        ef = name + '-1' + ext  # expected filename
        self.assertEquals(nf, ef)
