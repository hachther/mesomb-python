import unittest

from pymesomb import mesomb
from pymesomb.operations import WalletOperation


class WalletTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.provider_key = 'a1dc7a7391c538788043'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key ='fe8c2445-810f-4caa-95c9-778d51580163'

    def test_create_wallet(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.create_wallet(
            first_name='John',
            last_name='Doe',
            email='contact@gmail.com',
            phone_number='+237677550000',
            country='CM',
            gender='MAN'
        )

        self.assertEqual(wallet.first_name, 'John')
        self.assertEqual(wallet.last_name, 'Doe')
        self.assertEqual(wallet.email, 'contact@gmail.com')
        self.assertEqual(wallet.phone_number, '+237677550000')
        self.assertEqual(wallet.country, 'CM')
        self.assertEqual(wallet.gender, 'MAN')
        self.assertIsNotNone(wallet.number)

    def test_create_wallet_with_min_data(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.create_wallet(last_name='Doe', phone_number='+237677550000', gender='MAN')

        self.assertEqual(wallet.last_name, 'Doe')
        self.assertEqual(wallet.phone_number, '+237677550000')
        self.assertEqual(wallet.country, 'CM')
        self.assertEqual(wallet.gender, 'MAN')
        self.assertIsNotNone(wallet.number)

    def test_get_wallet(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.get_wallet(228)

        self.assertEqual(wallet.id, 228)
        self.assertEqual(wallet.first_name, 'John')
        self.assertEqual(wallet.last_name, 'Doe')
        self.assertEqual(wallet.email, 'contact@gmail.com')
        self.assertEqual(wallet.phone_number, '+237677550000')
        self.assertEqual(wallet.country, 'CM')
        self.assertEqual(wallet.gender, 'MAN')
        self.assertIsNotNone(wallet.number)

    def test_update_wallet(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.update_wallet(228, first_name='Jane', last_name='Doe', gender='MALE', phone_number='+237677550000')
        self.assertEqual(wallet.first_name, 'Jane')
        self.assertEqual(wallet.last_name, 'Doe')
        self.assertEqual(wallet.gender, 'MALE')
        self.assertEqual(wallet.phone_number, '+237677550000')

    def test_add_money_to_wallet(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.get_wallet(228)
        transaction = operation.add_money(228, amount=1000)

        self.assertEqual(transaction.direction, 1)
        self.assertEqual(transaction.status, 'SUCCESS')
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.balance_after, (wallet.balance or 0) + 1000)
        self.assertEqual(transaction.wallet, 228)
        self.assertEqual(transaction.country, 'CM')
        self.assertIsNotNone(transaction.fin_trx_id)
        self.assertIsNotNone(transaction.date)

    def test_add_remove_to_wallet(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        wallet = operation.get_wallet(228)
        transaction = operation.remove_money(228, amount=1000)

        self.assertEqual(transaction.direction, -1)
        self.assertEqual(transaction.status, 'SUCCESS')
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.balance_after, (wallet.balance or 0) - 1000)
        self.assertEqual(transaction.wallet, 228)
        self.assertEqual(transaction.country, 'CM')
        self.assertIsNotNone(transaction.fin_trx_id)
        self.assertIsNotNone(transaction.date)

    def test_list_transactions(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        transactions = operation.list_transactions(1)

        self.assertGreater(transactions.count, 0)
        # self.assertIsNotNone(transactions.next)
        self.assertIsNone(transactions.previous)
        self.assertTrue(len(transactions.results) > 0)

    def test_get_transactions(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        transactions = operation.get_transactions([1047, 1048])

        self.assertGreater(len(transactions), 0)

        transactions = operation.get_transactions(['REF-1'], source='EXTERNAL')

        self.assertGreater(len(transactions), 0)

    def test_get_transaction(self):
        operation = WalletOperation(self.provider_key, self.access_key, self.secret_key)

        transaction = operation.get_transaction(3061)

        self.assertEqual(transaction.id, 3061)
        self.assertEqual(transaction.direction, -1)
        self.assertEqual(transaction.status, 'SUCCESS')
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.balance_after, 1000)
        self.assertEqual(transaction.wallet, 228)
        self.assertEqual(transaction.country, 'CM')
        self.assertIsNotNone(transaction.fin_trx_id)
        self.assertIsNotNone(transaction.date)