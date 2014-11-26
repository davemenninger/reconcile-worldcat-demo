import reconcile
import unittest

class ReconcileTestCase(unittest.TestCase):

    def setUp(self):
        self.app = reconcile.app.test_client()

    def test_empty_search(self):
        rv = self.app.get('/reconcile')
        assert 'Worldcat Title Reconciliation Service' in rv.data

    def test_single_search(self):
        rv = self.app.post('/reconcile', data=dict(query='earthsea'), follow_redirects=True)
        assert 'A wizard of earthsea' in rv.data

if __name__ == '__main__':
    unittest.main()
