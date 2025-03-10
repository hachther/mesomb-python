import unittest

from pymesomb import mesomb
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException
from pymesomb.operations import FundraisingOperation


class Contribution(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.fund_key = 'fa78bded201b791712ee398c7ddfb8652669404f'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_make_payment_with_not_found_service(self):
        operation = FundraisingOperation(self.fund_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.make_contribution(amount=5, service='MTN', payer='670000000',
                                        full_name={'first_name': 'John', 'last_name': 'Doe'},
                                        contact={'email': 'contact@gmail.com', 'phone_number': '+237677550203'})

    def test_make_payment_with_permission_denied(self):
        operation = FundraisingOperation(self.fund_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.make_contribution(amount=5, service='MTN', payer='670000000',
                                        full_name={'first_name': 'John', 'last_name': 'Doe'},
                                        contact={'email': 'contact@gmail.com', 'phone_number': '+237677550203'})

    def test_make_payment_with_invalid_amount(self):
        operation = FundraisingOperation(self.fund_key, self.access_key, self.secret_key)
        with self.assertRaises(InvalidClientRequestException):
            operation.make_contribution(amount=5, service='MTN', payer='670000000',
                                        full_name={'first_name': 'John', 'last_name': 'Doe'},
                                        contact={'email': 'contact@gmail.com', 'phone_number': '+237677550203'})

    def test_make_contribution_success(self):
        operation = FundraisingOperation(self.fund_key, self.access_key, self.secret_key)
        response = operation.make_contribution(amount=100, service='MTN', payer='670000000',
                                               full_name={'first_name': 'John', 'last_name': 'Doe'},
                                               contact={'email': 'contact@gmail.com', 'phone_number': '+237677550203'})
        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_contribution_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.contribution.amount, 98)
        self.assertEqual(response.contribution.fees, 2)
        self.assertEqual(response.contribution.b_party, "237670000000")
        self.assertEqual(response.contribution.country, "CM")
        self.assertEqual(response.contribution.currency, "XAF")
        self.assertEqual(response.contribution.contributor.phone, "+237677550203")
        self.assertEqual(response.contribution.contributor.email, "contact@gmail.com")
        self.assertEqual(response.contribution.contributor.first_name, "John")
        self.assertEqual(response.contribution.contributor.last_name, "Doe")

    def test_make_contribution_anonymously_success(self):
        operation = FundraisingOperation(self.fund_key, self.access_key, self.secret_key)
        response = operation.make_contribution(amount=100, service='MTN', payer='670000000', anonymous=True)

        self.assertTrue(response.is_operation_success())
        self.assertTrue(response.is_contribution_success())
        self.assertEqual(response.status, "SUCCESS")
        self.assertEqual(response.contribution.amount, 98)
        self.assertEqual(response.contribution.fees, 2)
        self.assertEqual(response.contribution.b_party, "237670000000")
        self.assertEqual(response.contribution.country, "CM")
        self.assertEqual(response.contribution.currency, "XAF")
        self.assertIsNone(response.contribution.contributor)


class ContributionTest(unittest.TestCase):
    def setUp(self):
        mesomb.host = 'http://127.0.0.1:8000'
        self.fund_key = 'fa78bded201b791712ee398c7ddfb8652669404f'
        self.access_key = 'c6c40b76-8119-4e93-81bf-bfb55417b392'
        self.secret_key = 'fe8c2445-810f-4caa-95c9-778d51580163'

    def test_get_contributions_with_no_found_service(self):
        operation = FundraisingOperation(self.fund_key + 'f', self.access_key, self.secret_key)
        with self.assertRaises(ServiceNotFoundException):
            operation.get_contributions(['c6c40b76-8119-4e93-81bf-bfb55417b392'])

    def test_get_contributions_with_permission_denied(self):
        operation = FundraisingOperation(self.fund_key, 'f' + self.access_key, self.secret_key)
        with self.assertRaises(PermissionDeniedException):
            operation.get_contributions(['c6c40b76-8119-4e93-81bf-bfb55417b392'])

    def test_get_contributions_success(self):
        operation = FundraisingOperation(self.fund_key, self.access_key, self.secret_key)
        contributions = operation.get_contributions(['0685831f-4145-4352-ae81-155fec42c748'])
        self.assertEqual(1, len(contributions))

    def test_check_contributions_success(self):
        operation = FundraisingOperation(self.fund_key, self.access_key, self.secret_key)
        contributions = operation.check_contributions(['0685831f-4145-4352-ae81-155fec42c748'])
        self.assertEqual(1, len(contributions))
