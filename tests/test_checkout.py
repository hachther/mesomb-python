import unittest
from unittest.mock import patch

from pymesomb.models import CheckoutSession
from pymesomb.operations import CheckOutOperation
from pymesomb.params import PaymentLineItemPayload


def build_checkout_session_payload(**overrides):
    payload = {
        'id': 'cs_123',
        'object': 'checkout.session',
        'status': 'created',
        'amount': 1200,
        'amount_total': 1200,
        'currency': 'XAF',
        'description': 'Order #1001',
        'url': 'https://checkout.local/session/cs_123',
        'success_url': 'https://merchant.local/success',
        'cancel_url': 'https://merchant.local/cancel',
        'allowed_payment_methods': ['MTN', 'ORANGE'],
        'attempt_count': 0,
        'failure_code': None,
        'failure_message': None,
        'line_items': [
            {
                'product': 'prod_001',
                'unit_amount': 1200,
                'quantity': 1,
                'currency': 'XAF',
                'adjustable': False,
            }
        ],
        'metadata': {'order_id': '1001'},
        'branding_settings': {'display_name': 'My Shop'},
        'client_reference_id': 'ORD-1001',
        'secure_pay_mode': 'optional',
        'expires_at': '2026-05-06T10:00:00Z',
        'created_at': '2026-05-06T09:00:00Z',
        'updated_at': '2026-05-06T09:00:00Z',
    }
    payload.update(overrides)
    return payload


class CheckoutAlignmentTest(unittest.TestCase):
    def test_checkout_session_parses_line_items(self):
        session = CheckoutSession(build_checkout_session_payload())

        self.assertEqual(session.id, 'cs_123')
        self.assertEqual(len(session.line_items), 1)
        self.assertEqual(session.line_items[0].product, 'prod_001')
        self.assertEqual(session.line_items[0].unit_amount, 1200)
        self.assertEqual(session.line_items[0].quantity, 1)
        self.assertEqual(session.secure_pay_mode, 'optional')

        # Backward compatibility alias.
        self.assertIs(session.products, session.line_items)

    def test_checkout_session_accepts_legacy_products_key(self):
        payload = build_checkout_session_payload(line_items=[])
        payload['products'] = [
            {
                'product': {'id': 'prod_legacy', 'name': 'Legacy Product'},
                'unit_amount': 500,
                'quantity': 2,
                'currency': 'XAF',
            }
        ]

        session = CheckoutSession(payload)

        self.assertEqual(len(session.line_items), 1)
        self.assertEqual(session.line_items[0].product_id, 'prod_legacy')
        self.assertEqual(session.line_items[0].quantity, 2)

    def test_checkout_create_sends_line_items_and_fees_included(self):
        operation = CheckOutOperation('app_key', 'access_key', 'secret_key')

        line_items: list[PaymentLineItemPayload] = [
            {
                'product': 'prod_001',
                'unit_amount': 1200,
                'quantity': 1,
                'currency': 'XAF',
            }
        ]

        with patch.object(CheckOutOperation, 'execute_request', return_value=build_checkout_session_payload()) as mocked:
            session = operation.create(
                amount='1200',
                success_url='https://merchant.local/success',
                cancel_url='https://merchant.local/cancel',
                nonce='fixed-nonce',
                line_items=line_items,
                fees_included=False,
                secure_pay={
                    'terms_accepted': True,
                    'pay_mode': 'optional',
                    'dispute_enabled': True,
                },
            )

        args = mocked.call_args.args
        self.assertEqual(args[0], 'POST')
        self.assertEqual(args[1], 'checkout/sessions/')
        self.assertEqual(args[3], 'fixed-nonce')

        body = args[4]
        self.assertEqual(body['line_items'], line_items)
        self.assertFalse(body['fees_included'])
        self.assertEqual(body['secure_pay']['pay_mode'], 'optional')
        self.assertTrue(body['secure_pay']['terms_accepted'])
        self.assertEqual(body['mode'], 'payment')
        self.assertEqual(body['currency'], 'XAF')

        self.assertEqual(session.id, 'cs_123')


if __name__ == '__main__':
    unittest.main()

