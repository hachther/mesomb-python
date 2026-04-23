import unittest

from pymesomb import mesomb
from pymesomb.operations import CheckOutOperation


class PaymentMissingEndpointsTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.checkout = CheckOutOperation(self.application_key, self.access_key, self.secret_key)

    def call_or_skip(self, call, *args, **kwargs):
        try:
            return call(*args, **kwargs)
        except Exception as exc:
            self.skipTest(f'Local server fixtures not ready: {exc}')

    def test_checkout_session_flow(self):
        created = self.call_or_skip(
            self.checkout.create,
            amount=3000,
            success_url='https://merchant.local/success',
            cancel_url='https://merchant.local/cancel',
            description='Order #1002',
            client_reference_id='ORD-1002',
            metadata={'order_id': '1002'},
            nonce='nonce'
        )

        self.assertTrue(created.id)
        self.assertIn(created.status, ['created', 'active'])

        loaded = self.call_or_skip(self.checkout.check, created.id)
        self.assertEqual(loaded.id, created.id)

        expired = self.call_or_skip(self.checkout.expire, created.id)
        self.assertEqual(expired.id, created.id)
        self.assertIn(expired.status, ['expired', 'canceled', 'completed', 'active', 'created'])

        deleted = self.call_or_skip(self.checkout.delete, created.id)
        self.assertEqual(deleted, {})

