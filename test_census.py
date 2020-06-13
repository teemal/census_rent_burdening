import unittest
from unittest import mock
from census import Census

@unittest.mock.patch.dict('os.environ', { 'CENSUS_API_KEY': '1234' })
class TestCensus(unittest.TestCase):
    
    def setUp(self):
        self.census = Census()
        return super().setUp()

    def test_returns_api_key(self):
        """
        Test that it accepts correct year
        """
        census_key = self.census.get_census_api_key()
        self.assertEqual(census_key, '1234')


if __name__ == '__main__':
    unittest.main()