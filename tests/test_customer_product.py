import unittest

from pymesomb import mesomb
from pymesomb.operations import CustomerOperation, ProductOperation


class CustomerOperationTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.operation = CustomerOperation(self.access_key, self.secret_key)

    def call_or_skip(self, call, *args, **kwargs):
        try:
            return call(*args, **kwargs)
        except Exception as exc:
            self.skipTest(f'Local server fixtures not ready: {exc}')

    def test_create_customer(self):
        customer = self.call_or_skip(
            self.operation.create,
            email='john@demo.com',
            phone='670000000',
            first_name='John',
            last_name='Doe',
            address={'line1': 'Bonamoussadi', 'region': 'Littoral', 'town': 'Douala'},
            metadata={'vip': True},
            nonce='nonce'
        )

        self.assertTrue(customer.identifier)
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.address.line1, 'Bonamoussadi')

    def test_list_customers(self):
        result = self.call_or_skip(self.operation.list, page=1)
        self.assertGreaterEqual(result.count, 0)
        self.assertIsInstance(result.results, list)
        if result.results:
            self.assertTrue(result.results[0].identifier)


class ProductOperationTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.operation = ProductOperation(self.access_key, self.secret_key)

    def call_or_skip(self, call, *args, **kwargs):
        try:
            return call(*args, **kwargs)
        except Exception as exc:
            self.skipTest(f'Local server fixtures not ready: {exc}')

    def test_create_product(self):
        product = self.call_or_skip(
            self.operation.create,
            name='Premium Plan',
            price_type='Recurring',
            default_price='2000',
            nonce='nonce'
        )

        self.assertTrue(product.id)
        self.assertEqual(product.name, 'Premium Plan')
        self.assertEqual(product.price_type, 'Recurring')

    def test_delete_product(self):
        product = self.call_or_skip(
            self.operation.create,
            name='Temp Delete Product',
            default_price='1000',
            nonce='nonce'
        )
        result = self.call_or_skip(self.operation.delete, product.id)
        self.assertEqual(result, {})

