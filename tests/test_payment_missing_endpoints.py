import unittest
from unittest.mock import patch

from pymesomb import mesomb
from pymesomb.operations import PaymentOperation


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = ''

    def json(self):
        return self._payload


class PaymentMissingEndpointsTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'
        self.operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)

    @patch('pymesomb.operations.requests.request')
    def test_check_contact_info(self, request_mock):
        request_mock.return_value = MockResponse(200, {
            'first_name': 'John',
            'last_name': 'Doe'
        })

        response = self.operation.check_contact_info(service_key='670000000', provider='MTN', nonce='nonce')

        self.assertEqual(response.first_name, 'John')
        self.assertEqual(response.last_name, 'Doe')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'POST')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/payment/contact/info/')
        self.assertEqual(kwargs['json']['service_key'], '670000000')
        self.assertEqual(kwargs['json']['provider'], 'MTN')
        self.assertEqual(kwargs['json']['country'], 'CM')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

    @patch('pymesomb.operations.requests.request')
    def test_get_pricing(self, request_mock):
        request_mock.return_value = MockResponse(200, {
            'key': self.application_key,
            'name': 'My App'
        })

        response = self.operation.get_pricing()

        self.assertEqual(response.key, self.application_key)
        self.assertEqual(response.name, 'My App')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'GET')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/payment/pricing/')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

    @patch('pymesomb.operations.requests.request')
    def test_check_session(self, request_mock):
        request_mock.return_value = MockResponse(200, {
            'id': 'cs_123',
            'object': 'checkout.session',
            'status': 'active',
            'amount': 2500,
            'currency': 'XAF',
            'description': 'Order #1001',
            'checkout_url': 'https://checkout.local/session/cs_123',
            'success_url': 'https://merchant.local/success',
            'cancel_url': 'https://merchant.local/cancel',
            'allowed_payment_methods': ['MTN', 'ORANGE'],
            'customer': {
                'identifier': 'cust_1',
                'last_name': 'Doe',
                'first_name': 'John'
            },
            'attempt_count': 0,
            'failure_code': None,
            'failure_message': None,
            'products': [{
                'product': {'id': 'prod_1', 'name': 'Pro Pack'},
                'quantity': 1,
                'unit_price': '2500',
                'subtotal': '2500'
            }],
            'metadata': {'order_id': '1001'},
            'client_reference_id': 'ORD-1001',
            'expires_at': '2026-04-20T12:00:00Z',
            'created_at': '2026-04-20T11:00:00Z',
            'updated_at': '2026-04-20T11:30:00Z'
        })

        response = self.operation.check_session('cs_123')

        self.assertEqual(response.id, 'cs_123')
        self.assertEqual(response.status, 'active')
        self.assertEqual(response.customer.identifier, 'cust_1')
        self.assertEqual(len(response.products), 1)
        self.assertEqual(response.products[0].product.id, 'prod_1')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'GET')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/checkout/sessions/cs_123/')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

    @patch('pymesomb.operations.requests.request')
    def test_create_checkout_session(self, request_mock):
        request_mock.return_value = MockResponse(201, {
            'id': 'cs_124',
            'object': 'checkout.session',
            'status': 'created',
            'amount': 3000,
            'currency': 'XAF',
            'description': 'Order #1002',
            'checkout_url': 'https://checkout.local/session/cs_124',
            'success_url': 'https://merchant.local/success',
            'cancel_url': 'https://merchant.local/cancel',
            'allowed_payment_methods': ['MTN'],
            'customer': {
                'identifier': 'cust_2',
                'last_name': 'Smith'
            },
            'attempt_count': 0,
            'failure_code': None,
            'failure_message': None,
            'products': [],
            'metadata': {'order_id': '1002'},
            'client_reference_id': 'ORD-1002',
            'expires_at': '2026-04-20T12:30:00Z',
            'created_at': '2026-04-20T11:30:00Z',
            'updated_at': '2026-04-20T11:30:00Z'
        })

        response = self.operation.create_checkout_session(
            amount=3000,
            success_url='https://merchant.local/success',
            cancel_url='https://merchant.local/cancel',
            description='Order #1002',
            client_reference_id='ORD-1002',
            metadata={'order_id': '1002'},
            nonce='nonce'
        )

        self.assertEqual(response.id, 'cs_124')
        self.assertEqual(response.status, 'created')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'POST')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/checkout/sessions/')
        self.assertEqual(kwargs['json']['amount'], 3000)
        self.assertEqual(kwargs['json']['success_url'], 'https://merchant.local/success')
        self.assertEqual(kwargs['json']['cancel_url'], 'https://merchant.local/cancel')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

    @patch('pymesomb.operations.requests.request')
    def test_expire_checkout_session(self, request_mock):
        request_mock.return_value = MockResponse(200, {
            'id': 'cs_125',
            'object': 'checkout.session',
            'status': 'expired',
            'amount': 1000,
            'currency': 'XAF',
            'description': None,
            'checkout_url': 'https://checkout.local/session/cs_125',
            'success_url': 'https://merchant.local/success',
            'cancel_url': 'https://merchant.local/cancel',
            'allowed_payment_methods': ['MTN'],
            'customer': {
                'identifier': 'cust_3',
                'last_name': 'User'
            },
            'attempt_count': 0,
            'failure_code': None,
            'failure_message': None,
            'products': [],
            'metadata': {},
            'client_reference_id': None,
            'expires_at': '2026-04-20T12:00:00Z',
            'created_at': '2026-04-20T11:00:00Z',
            'updated_at': '2026-04-20T11:59:59Z'
        })

        response = self.operation.expire_checkout_session('cs_125')

        self.assertEqual(response.id, 'cs_125')
        self.assertEqual(response.status, 'expired')

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'PATCH')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/checkout/sessions/cs_125/expire/')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

    @patch('pymesomb.operations.requests.request')
    def test_delete_checkout_session(self, request_mock):
        request_mock.return_value = MockResponse(204, {})

        response = self.operation.delete_checkout_session('cs_126')

        self.assertEqual(response, {})

        args, kwargs = request_mock.call_args
        self.assertEqual(args[0], 'DELETE')
        self.assertEqual(args[1], 'http://127.0.0.1:8000/api/v1.1/checkout/sessions/cs_126/')
        self.assertEqual(kwargs['headers']['X-MeSomb-Application'], self.application_key)
        self.assertIn('Authorization', kwargs['headers'])

