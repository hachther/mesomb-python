import unittest
from datetime import datetime

from pymesomb import mesomb
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException
from pymesomb.models import Wallet
from pymesomb.operations import PaymentOperation, WalletOperation
from pymesomb.utils import RandomGenerator


class CollectTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://192.168.100.10:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_make_payment_with_not_found_service(self):
        operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.make_collect({'amount': 5, 'service': 'MTN', 'payer': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_payment_with_permission_denied(self):
        operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.make_collect({'amount': 5, 'service': 'MTN', 'payer': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_payment_with_invalid_amount(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        with self.assertRaises(InvalidClientRequestException):
            operation.make_collect({'amount': 5, 'service': 'MTN', 'payer': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_payment_success(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_collect({
            'amount': 100,
            'service': 'MTN',
            'payer': '670000000',
            'date': datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'trxID': '1'
        })
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_transaction_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.transaction.amount, 98)
        self.assertEqual(response.transaction.fees, 2)
        self.assertEqual(response.transaction.b_party, "237670000000")
        self.assertEqual(response.transaction.country, "CM")
        self.assertEqual(response.transaction.currency, "XAF")
        self.assertEqual(response.transaction.reference, "1")

    def test_make_payment_success_and_products(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_collect({
            'amount': 100,
            'service': 'MTN',
            'payer': '670000000',
            'date': datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'trxID': '1',
            'customer': {
                'phone': '+237677550439',
                'email': 'fisher.bank@gmail.com',
                'first_name': 'Fisher',
                'last_name': 'BANK',
            },
            'location': {
                'town': 'Douala',
                'country': 'Cameroun'
            },
            'products': [
                {
                    'id': 'SKU001',
                    'name': 'Sac a Main',
                    'category': 'Sac',
                }
            ]
        })
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_transaction_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.transaction.amount, 98.0)
        self.assertEqual(response.transaction.fees, 2)
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
        self.assertEqual(len(response.transaction.products), 1)

    def test_make_payment_pending(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_collect({
            'amount': 100,
            'service': 'MTN',
            'payer': '670000000',
            'date': datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'mode': 'asynchronous'
        })
        self.assertTrue(response.is_operation_success())
        self.assertFalse(response.is_transaction_success())
        self.assertEqual(response.transaction.status, "PENDING")


class DepositTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://192.168.100.10:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_make_deposit_with_not_found_service(self):
        operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.make_deposit({'amount': 5, 'service': 'MTN', 'receiver': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_deposit_with_permission_denied(self):
        operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.make_deposit({'amount': 5, 'service': 'MTN', 'receiver': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_deposit_with_invalid_amount(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        with self.assertRaises(InvalidClientRequestException):
            operation.make_deposit({'amount': 5, 'service': 'MTN', 'receiver': '670000000', 'nonce': 'ifshdifsdf'})

    def test_make_deposit_success(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        response = operation.make_deposit({
            'amount': 100,
            'service': 'MTN',
            'receiver': '670000000',
            'date': datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'trxID': '1'
        })
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_transaction_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.transaction.amount, 100)
        self.assertEqual(response.transaction.fees, 0)
        self.assertEqual(response.transaction.b_party, "237670000000")
        self.assertEqual(response.transaction.country, "CM")
        self.assertEqual(response.transaction.currency, "XAF")
        self.assertEqual(response.transaction.reference, "1")


class SecurityTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://192.168.100.10:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_unset_blacklist_ips(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        application = operation.update_security('blacklist_receivers', 'UNSET')
        self.assertIsNone(application.get_security_field('whitelist_ips'))

    def test_unset_blacklist_receivers(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        application = operation.update_security('blacklist_receivers', 'UNSET')
        self.assertIsNone(application.get_security_field('blacklist_receivers'))


class StatusTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://192.168.100.10:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_get_status_with_no_found_service(self):
        operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.get_status()

    def test_get_status_with_permission_denied(self):
        operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.get_status()

    def test_get_status_success(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        application = operation.get_status()
        self.assertEqual(application.name, 'Meudocta Shop')
        self.assertListEqual(application.countries, ['CM', 'NE'])


class UtilTest(unittest.TestCase):
    def test_operator_detect(self):
        from pymesomb.utils import detect_operator

        self.assertEqual(detect_operator('677559230'), 'MTN')
        self.assertEqual(detect_operator('237677559230'), 'MTN')
        self.assertEqual(detect_operator('690090980'), 'ORANGE')
        self.assertEqual(detect_operator('237690090980'), 'ORANGE')


class TransactionTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://192.168.100.10:8000'
        self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_get_transactions_with_no_found_service(self):
        operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.get_transactions(['c6c40b76-8119-4e93-81bf-bfb55417b392'])

    def test_get_transactions_with_permission_denied(self):
        operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.get_transactions(['c6c40b76-8119-4e93-81bf-bfb55417b392'])

    def test_get_transactions_success(self):
        operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
        transactions = operation.get_transactions(['9886f099-dee2-4eaa-9039-e92b2ee33353'])
        self.assertEqual(1, len(transactions))


class WalletTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.provider_key = 'a1dc7a7391c538788043'
        self.access_key = '28823cb9-0caf-4d6d-84ca-4d7b94aad353'
        self.secret_key = '3043b689-b37d-4c45-ac5a-bda19b04f559'

    def test_operations(self):

        # Create wallet
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)
        identifier = 59
        wallet = operation.create_wallet({
            'first_name': 'Vigny',
            'last_name': 'GHOTOU',
            'phone_number': '+237677559230',
            'nonce': RandomGenerator.nonce(),
        })
        self.assertIsNotNone(wallet.number)
        self.assertEqual(wallet.balance, 0)
        identifier = wallet.identifier

        # Get Wallet
        wallet = operation.get_wallet(identifier)
        self.assertIsNotNone(wallet.number)

        wallet = operation.update_wallet(identifier, {
            'first_name': 'Daniel',
            'last_name': 'Smith',
            'nonce': RandomGenerator.nonce(),
        })
        wallet = operation.get_wallet(identifier)
        self.assertIsNotNone(wallet.number)
        self.assertEqual(wallet.first_name, u'Daniel')
        self.assertEqual(wallet.last_name, u'Smith')

        wallets = operation.list_wallets()
        self.assertGreater(wallets['count'], 0)
        self.assertGreater(len(wallets['results']), 0)

        ret = operation.adjust_wallet(identifier, {
            'amount': 200,
            'direction': 1,
            'nonce': RandomGenerator.nonce(),
        })
        self.assertEqual(ret['wallet'].balance, 200)

        ret = operation.adjust_wallet(identifier, {
            'amount': 200,
            'direction': -1,
            'nonce': RandomGenerator.nonce(),
        })
        self.assertEqual(ret['wallet'].balance, 0)

        ret = operation.adjust_wallet(identifier, {
            'amount': 200,
            'direction': -1,
            'force': True,
            'nonce': RandomGenerator.nonce(),
        })
        self.assertEqual(ret['wallet'].balance, -200)

        operation.delete_wallet(identifier)



