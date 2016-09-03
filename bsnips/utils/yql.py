"""A small sample of the YQL API interactions.
YQL documentation: https://developer.yahoo.com/yql/
"""
import requests


class YQL(object):
    base_url = 'http://query.yahooapis.com/v1/'

    def is_authorized(self):
        return False

    def _get_params(self, **kwargs):
        default = {
            'q': '',
            'format': 'json',
            'callback': '',
            'crossProduct': 'optimized',
            # 'diagnostics': 'true',
            'diagnostics': 'false',
            'debug': '',
            'env': "store://datatables.org/alltableswithkeys",
            'jsonCompat': 'new'
        }
        default.update({k: v for k, v in kwargs.iteritems() if k in default})
        return default

    def _get_data(self, **kwargs):
        if self.is_authorized():
            url = self.base_url + 'yql'
        else:
            url = self.base_url + 'public/yql'
        r = requests.get(url, params=self._get_params(**kwargs))
        return r.json()

    def xchange(self, *args):
        assert len(args) % 2 == 0
        currency_list = []
        curr1_curr_2 = ''
        for i, curr in enumerate(args, 1):
            if i % 2 != 0:
                curr1_curr_2 = curr
            else:
                curr1_curr_2 += curr
                currency_list.append('"' + curr1_curr_2 + '"')
        q = 'select * from yahoo.finance.xchange where pair in (%s)' % ', '.join(currency_list)
        return self._get_data(q=q)


if __name__ == "__main__":
    from pprint import pprint
    from bsnips.utils.log import setup_logging

    setup_logging()
    yql = YQL()
    pprint(yql.xchange('USD', 'KES'))
