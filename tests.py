import unittest
from datetime import datetime

from pymesomb import settings
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException
from pymesomb.operations import PaymentOperation
from pymesomb.signature import Signature


class CollectTest(unittest.TestCase):
  def setUp(self):
    settings.host = 'http://127.0.0.1:8000'
    self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
    self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
    self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

  def test_make_payment_with_not_found_service(self):
    operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
    with self.assertRaises(ServiceNotFoundException):
      operation.make_collect(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_payment_with_permission_denied(self):
    operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
    with self.assertRaises(PermissionDeniedException):
      operation.make_collect(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_payment_with_invalid_amount(self):
    operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
    with self.assertRaises(InvalidClientRequestException):
      operation.make_collect(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_payment_success(self):
    operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
    response = operation.make_collect(100, 'MTN', '677550203', datetime.now(), Signature.generate_nonce())
    self.assertTrue(response.is_operation_success())
    self.assertTrue(response.is_transaction_success())

  def test_make_payment_pending(self):
    operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
    response = operation.make_collect(100, 'MTN', '677550203', datetime.now(), Signature.generate_nonce(), mode='asynchronous')
    self.assertTrue(response.is_operation_success())
    self.assertFalse(response.is_transaction_success())


class DepositTest(unittest.TestCase):
  def setUp(self):
    settings.host = 'http://127.0.0.1:8000'
    self.application_key = '2bb525516ff374bb52545bf22ae4da7d655ba9fd'
    self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
    self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

  def test_make_deposit_with_not_found_service(self):
    operation = PaymentOperation(self.application_key + 'f', self.access_key, self.secret_key)
    with self.assertRaises(ServiceNotFoundException):
      operation.make_deposit(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_deposit_with_permission_denied(self):
    operation = PaymentOperation(self.application_key, 'f' + self.access_key, self.secret_key)
    with self.assertRaises(PermissionDeniedException):
      operation.make_deposit(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_deposit_with_invalid_amount(self):
    operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
    with self.assertRaises(InvalidClientRequestException):
      operation.make_deposit(5, 'MTN', '677550203', datetime.now(), 'ifshdifsdf')

  def test_make_deposit_success(self):
    operation = PaymentOperation(self.application_key, self.access_key, self.secret_key)
    response = operation.make_deposit(100, 'MTN', '677550203', datetime.now(), Signature.generate_nonce())
    self.assertTrue(response.is_operation_success())
    self.assertTrue(response.is_transaction_success())


class SecurityTest(unittest.TestCase):
  def setUp(self):
    settings.host = 'http://127.0.0.1:8000'
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
    settings.host = 'http://127.0.0.1:8000'
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


class TransactionTest(unittest.TestCase):
  def setUp(self):
    settings.host = 'http://127.0.0.1:8000'
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
