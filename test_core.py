import unittest, tempfile, json, sqlite3, copy
from pathlib import Path
import app as c

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.config = json.loads((Path(__file__).resolve().parent / 'scenario.json').read_text(encoding='utf-8'))

    def test_ambiguity(self):
        self.assertEqual(c.run(self.config)['review'][0]['reason'], 'ambiguous')

    def test_cash_conservation(self):
        for row in c.run(self.config)['cash_controls']:
            self.assertEqual(row['net_minor'], row['allocated_minor'] + row['unallocated_minor'])

    def test_explicit_multi(self):
        self.assertEqual(len(c.run(self.config)['allocations']), 2)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            c.reconcile(self.config['invoices'] * 2, [])

    def test_negative_fee(self):
        p = copy.deepcopy(self.config['payments'][0])
        p['fee_minor'] = -1
        with self.assertRaises(ValueError):
            c.reconcile(self.config['invoices'], [p])

    def test_cross_currency(self):
        cfg = copy.deepcopy(self.config)
        cfg['payments'][1]['currency'] = 'EUR'
        self.assertEqual(c.run(cfg)['allocations'], [])

    def test_partial(self):
        cfg = copy.deepcopy(self.config)
        cfg['payments'] = [cfg['payments'][0]]
        cfg['payments'][0]['invoice_refs'] = ['I1']
        self.assertEqual(c.run(cfg)['balances'][0]['open_minor'], 5000)

    def test_invalid_reference(self):
        cfg = copy.deepcopy(self.config)
        cfg['payments'][1]['invoice_refs'] = ['missing']
        self.assertEqual(c.run(cfg)['review'][1]['reason'], 'invalid_or_closed_reference')
if __name__ == '__main__':
    unittest.main()
