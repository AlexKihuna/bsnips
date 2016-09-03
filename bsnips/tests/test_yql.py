from unittest import TestCase
from bsnips.utils.yql import YQL


class TestYQL(TestCase):
    def setUp(self):
        self.yql = YQL()

    def test_xchange(self):
        r = self.yql.xchange('USD', 'KES', 'GBP', 'KES')
        self.assertIn('query', r)
        self.assertIn('count', r['query'])
        self.assertIn('results', r['query'])
        self.assertIn('rate', r['query']['results'])
        count = r['query']['count']
        rate = r['query']['results']['rate']
        if count == 1:
            self.assertTrue(isinstance(rate, dict))
        else:
            self.assertTrue(isinstance(rate, list))
            self.assertEquals(count, len(rate))
