import unittest
from unittest.mock import patch

from pymesomb import mesomb
from pymesomb.operations import CustomerOperation, ProductOperation


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = ''

    def json(self):
        return self._payload


class CustomerOperationTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.operation = CustomerOperation(self.application_key, self.access_key, self.secret_key)

    @patch('pymesomb.operations.requests.request')
    def test_create_customer(self, request_mock):
        request_mock.return_value = MockResponse(201, {
            'identifier': 'cust_1',
            'email': 'john@demo.com',
            'phone': '670000000',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': {
                'line1': 'Bonamoussadi',
                'region': 'Littoral',
                'town': 'Douala'
            },
            'metadata': {'vip': True}
        })

        customer = self.operation.create(
            email='john@demo.com',
            phone='670000000',
            first_name='John',
            last_name='Doe',
            address={'line1': 'Bonamoussadi', 'region': 'Littoral', 'town': 'Douala'},
            metadata={'vip': True},
            nonce='nonce'
        )

        self.assertEqual(customer.identifier, 'cust_1')
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.address.line1, 'Bonamoussadi')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'POST')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/customers/')
        self.assertEqual(kwargs['json']['email'], 'john@demo.com')
        # self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)

    @patch('pymesomb.operations.requests.request')
    def test_list_customers(self, request_mock):
        request_mock.return_value = MockResponse(200, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'identifier': 'cust_1', 'last_name': 'Doe'}
            ]
        })

        result = self.operation.list(page=2)
        self.assertEqual(result.count, 1)
        self.assertEqual(result.results[0].identifier, 'cust_1')

        args, _ = request_mock.call_args
        self.assertEqual(args[0], 'GET')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/customers/?page=2')


class ProductOperationTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.operation = ProductOperation(self.application_key, self.access_key, self.secret_key)

    @patch('pymesomb.operations.requests.request')
    def test_create_product(self, request_mock):
        request_mock.return_value = MockResponse(201, {
            'id': 'prod_1',
            'name': 'Premium Plan',
            'price_type': 'Recurring',
            'default_price': '2000'
        })

        product = self.operation.create(
            name='Premium Plan',
            price_type='Recurring',
            default_price='2000',
            nonce='nonce'
        )

        self.assertEqual(product.id, 'prod_1')
        self.assertEqual(product.name, 'Premium Plan')
        self.assertEqual(product.price_type, 'Recurring')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'POST')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/products/')
        self.assertEqual(kwargs['json']['name'], 'Premium Plan')

    @patch('pymesomb.operations.requests.request')
    def test_delete_product(self, request_mock):
        request_mock.return_value = MockResponse(204, {})

        result = self.operation.delete('prod_1')
        self.assertEqual(result, {})

        args, _ = request_mock.call_args
        self.assertEqual(args[0], 'DELETE')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/products/prod_1/')
