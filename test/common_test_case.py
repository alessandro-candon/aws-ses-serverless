import unittest

from configuration import ENV
from entity.fixtures import populate_db
from entity.schema import mapping_database, define_database


class CommonTestCase(unittest.TestCase):
    def __init__(self, methodName='test'):
        super().__init__(methodName)
        self.database = define_database(ENV)

    def setUp(self):
        print("SetUp test")

    def tearDown(self):
        self.database.drop_all_tables(with_all_data=True)
        print("Tear Down test")
