import unittest

from entity.schema import define_database

ENV = 'test'


class CommonTestCase(unittest.TestCase):
    def setUp(self):
        self.database = define_database(ENV)
        print("SetUp test")

    def tearDown(self):
        self.database.drop_all_tables(with_all_data=True)
        print("Tear Down test")
