import unittest

from pymesomb import mesomb
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException
from pymesomb.operations import PaymentOperation


class YangoTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.application_key = '4a25f8788665924aa2905daf3b2700eb916c7d56'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_make_payment_with_not_found_service(self):
        operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.make_yango_refill(amount=5, service='MTN', payer='670000000', nonce='ifshdifsdf', driver_id='8cadabd4c759446a9f9e4042d628ee1f')

    def test_make_payment_with_permission_denied(self):
        operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.make_yango_refill(amount=5, service='MTN', payer='670000000', nonce='ifshdifsdf',
                                        driver_id='8cadabd4c759446a9f9e4042d628ee1f')

    def test_make_payment_with_invalid_amount(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        with self.assertRaises(InvalidClientRequestException):
            operation.make_yango_refill(amount=5, service='MTN', payer='670000000', nonce='ifshdifsdf',
                                        driver_id='8cadabd4c759446a9f9e4042d628ee1f')

    def test_make_payment_success(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_yango_refill(amount=100, service='MTN', payer='670000000', trx_id='1', driver_id='8cadabd4c759446a9f9e4042d628ee1f')
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_transaction_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.transaction.amount, 98.5)
        self.assertEqual(response.transaction.fees, 1.5)
        self.assertEqual(response.transaction.b_party, "237670000000")
        self.assertEqual(response.transaction.country, "CM")
        self.assertEqual(response.transaction.currency, "XAF")
        self.assertEqual(response.transaction.reference, "1")

    def test_make_payment_success_and_products(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_yango_refill(amount=100, service='MTN', payer='670000000', driver_id='8cadabd4c759446a9f9e4042d628ee1f', trx_id='1', customer={
            'phone': '+237677550439',
            'email': 'fisher.bank@gmail.com',
            'first_name': 'Fisher',
            'last_name': 'BANK',
        }, location={
            'town': 'Douala',
            'region': 'Littoral',
            'country': 'Cameroun'
        })
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_transaction_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.transaction.amount, 98.5)
        self.assertEqual(response.transaction.fees, 1.5)
        self.assertEqual(response.transaction.b_party, "237670000000")
        self.assertEqual(response.transaction.country, "CM")
        self.assertEqual(response.transaction.currency, "XAF")
        self.assertEqual(response.transaction.reference, "1")
        self.assertEqual(response.transaction.customer.phone, "+237677550439")
        self.assertEqual(response.transaction.customer.email, "fisher.bank@gmail.com")
        self.assertEqual(response.transaction.customer.first_name, "Fisher")
        self.assertEqual(response.transaction.customer.last_name, "BANK")
        self.assertEqual(response.transaction.location.town, "Douala")
        self.assertEqual(response.transaction.location.country, "Cameroun")

    def test_make_payment_pending(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_yango_refill(amount=100, service='MTN', payer='670000000', mode='asynchronous', driver_id='8cadabd4c759446a9f9e4042d628ee1f')
        self.assertTrue(response.is_operation_success())
        self.assertFalse(response.is_transaction_success())
        self.assertEqual(response.transaction.status, "PENDING")