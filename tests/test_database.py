import pandas as pd
from pathlib import Path
import unittest

from golf.params import *
from golf.golf_handicap_calculation.main import calculate_index


class TestDatabase(unittest.TestCase):
    # def test_index_table_type(self):
    #     index_table = calculate_index()
    #     self.assertIsInstance(index_table, pd.DataFrame)

    # def test_index_table_shape(self):
    #     index_table = calculate_index()
    #     self.assertEqual(index_table.shape[1], 18)

    # def test_database_created(self):
    #     self.assertTrue(Path(LOCAL_DATA_PATH).joinpath('golf.sqlite').exists())

    def test_folder_structure(self):
        self.assertTrue(Path(repo_path).joinpath("golf", "api").exists())
        self.assertTrue(Path(repo_path).joinpath("golf", "golf_handicap_calculation").exists())
        self.assertTrue(Path(repo_path).joinpath("golf", "database").exists())
        self.assertTrue(Path(repo_path).joinpath("golf", "oop").exists())
