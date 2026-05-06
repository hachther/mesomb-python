import json
from abc import ABC
from datetime import datetime
from typing import Optional, Dict, List, Any
try:
    from typing import Unpack
except ImportError:  # pragma: no cover
    from typing_extensions import Unpack

import requests

from pymesomb import mesomb, __version__
from pymesomb.models import (TransactionResponse, Application, Transaction, Wallet, PaginatedWallets,
                             WalletTransaction, PaginatedWalletTransactions, ContributionResponse, Contribution,
                             ContactVerificationResponse, PaymentAppResponse, Customer,
                             Product, PaginatedCustomers, PaginatedProducts, CheckoutSession)
from pymesomb.params import (CollectParams, DepositParams, AirtimeParams, YangoRefillParams, RefundParams,
                             ContactInfoParams, WalletCreateParams, WalletUpdateParams, WalletAddMoneyParams,
                             WalletRemoveMoneyParams, WalletTransferMoneyParams,
                             FundraisingContributionParams, CustomerParams, ProductCreateParams,
                             ProductUpdateParams, ProductPatchParams, CheckoutCreateParams)
from pymesomb.signature import Signature
from pymesomb.utils import RandomGenerator


class AOperation(ABC):
    """ """
    service = None

    def __init__(self, target, access_key, secret_key, language='en'):
        self.target = target
        self.access_key = access_key
        self.secret_key = secret_key
        self.language = language

    def process_client_exception(self, response):
        """
        Process exception from the client request

        Args:
            response: the response from the request

        Raises:
            ServiceNotFoundException: When the service is not found
            PermissionDeniedException: When the permission is denied
            InvalidClientRequestException: When the client request is invalid
            ServerException: When the server return an error
        """
        from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, \
            InvalidClientRequestException, ServerException

        status_code = response.status_code
        detail = response.text
        code = None

        if detail.startswith('{'):
            data = json.loads(detail)
            detail = data['detail']
            code = data['code']

        if status_code == 404:
            raise ServiceNotFoundException(detail, code)

        if status_code in [403, 401]:
            raise PermissionDeniedException(detail, code)

        if status_code == 400:
            raise InvalidClientRequestException(detail, code)

        raise ServerException(detail, code)

    def build_url(self, endpoint: str) -> str:
        """
        Build url to use in the request

        Args:
            endpoint (str): the endpoint to use in the request

        Returns:
            str: the full url to use in the request
        """
        return f'{mesomb.host}/api/{mesomb.api_version}/{endpoint}'

    def get_authorization(self, method: str, endpoint: str, date: datetime, nonce: str,
                          headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> str:
        """
        Get the authorization to use in the request

        Args:
            method (str): the HTTP method to use
            endpoint (str): the endpoint to use in the request
            date (datetime): the date of the request
            nonce (str): the nonce of the request
            headers (Optional[Dict[str, Any]]): the headers to use in the request (Default value = None)
            body (Optional[Dict[str, Any]]): the body to use in the request (Default value = None)

        Returns:
            str: the authorization to use in the request
        """
        if headers is None:
            headers = {}

        url = self.build_url(endpoint)

        credentials = {'access_key': self.access_key, 'secret_key': self.secret_key}

        return Signature.sign_request(self.service, method, url, date, nonce, credentials, headers, body)

    def execute_request(self, method: str, endpoint: str, date: datetime, nonce: str = '', body: Dict[str, Any] = None,
                        mode: Optional[str] = None):
        """
        Execute the request to the MeSomb API

        Args:
            method (str): the HTTP method to use
            endpoint (str): the endpoint to use in the request
            date (datetime): the date of the request
            nonce (str): the nonce of the request (Default value = '')
            body (Dict[str, Any]): the body to use in the request (Default value = None)
            mode (Optional[str]): the mode to use in the request (Default value = None)

        Returns:
            dict: the response of the request

        Raises:
            ServiceNotFoundException: When the service is not found
            PermissionDeniedException: When the permission is denied
            InvalidClientRequestException: When the client request is invalid
            ServerException: When the server return an error
        """
        url = self.build_url(endpoint)

        headers = {
            'x-mesomb-date': str(int(date.timestamp())),
            'x-mesomb-nonce': nonce,
            'Accept-Language': self.language,
            'X-MeSomb-Source': f'PyMeSomb/{__version__}',
        }

        if self.service == 'payment':
            headers['X-MeSomb-Application'] = self.target

        if self.service == 'fundraising':
            headers['X-MeSomb-Fund'] = self.target

        if self.service == 'wallet':
            headers['X-MeSomb-Provider'] = self.target

        if body and 'trxID' in body:
            headers['X-MeSomb-TrxID'] = str(body.pop('trxID'))

        if mode:
            headers['X-MeSomb-OperationMode'] = mode

        if method == 'POST':
            authorization = self.get_authorization(method, endpoint, date, nonce,
                                                   headers={'content-type': 'application/json'},
                                                   body=body)
        else:
            authorization = self.get_authorization(method, endpoint, date, nonce)

        headers['Authorization'] = authorization

        response = requests.request(method, url, json=body, headers=headers)

        status_code = response.status_code
        if status_code >= 400:
            self.process_client_exception(response)

        # Some endpoints (e.g. DELETE 204) return an empty body.
        try:
            return response.json()
        except ValueError:
            return {}


class PaymentOperation(AOperation):
    """
    Payment operation class to interact with the MeSomb payment service
    """
    service = 'payment'

    def __init__(self, application_key, access_key, secret_key):
        super().__init__(application_key, access_key, secret_key)

    def make_collect(self, **params: Unpack[CollectParams]) -> TransactionResponse:
        """Collect money from a payer account.

        Args:
            **params: Collection parameters defined in ``CollectParams``.

        Returns:
            TransactionResponse
        """

        endpoint = 'payment/collect/'

        body = {
            'amount': params['amount'],
            'payer': params['payer'],
            'fees': params.get('fees', True),
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
            'amount_currency': params.get('currency', 'XAF'),
            'conversion': params.get('conversion', False),
        }
        if params.get('trx_id'):
            body['trxID'] = params['trx_id']

        if params.get('location'):
            body['location'] = params['location']

        if params.get('customer'):
            body['customer'] = params['customer']

        if params.get('line_items'):
            body['line_items'] = params['line_items']

        return TransactionResponse(
            self.execute_request(
                'POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(),
                body, params.get('mode', 'synchronous')
            )
        )

    def make_deposit(self, **params: Unpack[DepositParams]) -> TransactionResponse:
        """
        Make a deposit to a receiver mobile account.

        Args:
            **params: Deposit parameters defined in ``DepositParams``.

        Returns:
            TransactionResponse
        """
        endpoint = 'payment/deposit/'

        body = {
            'amount': params['amount'],
            'receiver': params['receiver'],
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
            'amount_currency': params.get('currency', 'XAF'),
            'conversion': params.get('conversion', False),
        }

        if params.get('trx_id'):
            body['trxID'] = params['trx_id']

        if params.get('location'):
            body['location'] = params['location']

        if params.get('customer'):
            body['customer'] = params['customer']

        if params.get('line_items'):
            body['line_items'] = params['line_items']

        return TransactionResponse(
            self.execute_request('POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(), body)
        )

    def purchase_airtime(self, **params: Unpack[AirtimeParams]) -> TransactionResponse:
        """
        Purchase airtime for a receiver account.

        Args:
            **params: Airtime purchase parameters defined in ``AirtimeParams``.

        Returns:
            TransactionResponse
        """
        endpoint = 'payment/airtime/'

        body = {
            'amount': params['amount'],
            'receiver': params['receiver'],
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
            'amount_currency': params.get('currency', 'XAF'),
            'merchant': params['merchant'],
        }

        if params.get('trx_id'):
            body['trxID'] = params['trx_id']

        if params.get('location'):
            body['location'] = params['location']

        if params.get('customer'):
            body['customer'] = params['customer']

        if params.get('line_items'):
            body['line_items'] = params['line_items']

        return TransactionResponse(
            self.execute_request('POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(), body)
        )

    def make_yango_refill(self, **params: Unpack[YangoRefillParams]) -> TransactionResponse:
        """
        Method to refill a Yango account.

        Args:
            **params: Yango refill parameters defined in ``YangoRefillParams``.

        Returns:
          TransactionResponse

        """
        endpoint = 'payment/yango/refill/'

        body = {
            'amount': params['amount'],
            'payer': params['payer'],
            'service': params['service'],
            'driver_id': params['driver_id'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
            'amount_currency': params.get('currency', 'XAF'),
        }

        if params.get('trx_id'):
            body['trxID'] = params['trx_id']

        if params.get('location'):
            body['location'] = params['location']

        if params.get('customer'):
            body['customer'] = params['customer']

        if params.get('line_items'):
            body['line_items'] = params['line_items']

        return TransactionResponse(
            self.execute_request(
                'POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(),
                body, params.get('mode', 'synchronous')
            )
        )

    def get_status(self) -> Application:
        """Get the current status of your service on MeSomb

        Returns:
          Application

        """
        endpoint = 'payment/status/'

        return Application(self.execute_request('GET', endpoint, datetime.now()))

    def get_transactions(self, ids, source='MESOMB') -> List[Transaction]:
        """
        Get transactions from MeSomb by IDs.

        Args:
            source: source of the transactionID: MESOMB or EXTERNAL (Default value = 'MESOMB')
            ids: list of ids

        Returns:
            List[Transaction]
        """
        endpoint = f"payment/transactions/?{'&'.join([f'ids={id}' for id in ids])}&source={source}"

        return [Transaction(item) for item in self.execute_request('GET', endpoint, datetime.now())]

    def check_transactions(self, ids, source='MESOMB') -> List[Transaction]:
        """
        Check transactions from MeSomb by IDs.

        Args:
            source: source of the transactionID: MESOMB or EXTERNAL (Default value = 'MESOMB')
            ids: list of ids

        Returns:
            List[Transaction]
        """
        endpoint = f"payment/transactions/check/?ids={','.join(ids)}&source={source}"
        return [Transaction(item) for item in self.execute_request('GET', endpoint, datetime.now())]

    def refund_transaction(self, **params: Unpack[RefundParams]) -> TransactionResponse:
        """
        Refund a transaction in MeSomb

        Args:
            **params: Refund parameters defined in ``RefundParams``.
        Returns:
            TransactionResponse
        """
        endpoint = f'payment/refund/'

        body = {'id': params['trx_id']}
        if params.get('amount') is not None:
            body['amount'] = params['amount']
        if params.get('currency'):
            body['currency'] = params['currency']
            body['amount_currency'] = params['currency']
        if params.get('conversion') is not None:
            body['conversion'] = params['conversion']

        return TransactionResponse(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(),
                                                       body))

    def check_contact_info(self, **params: Unpack[ContactInfoParams]) -> ContactVerificationResponse:
        """
        Check subscriber basic information.

        Args:
            **params: Contact lookup parameters defined in ``ContactInfoParams``.

        Returns:
            ContactVerificationResponse
        """
        endpoint = 'payment/contact/info/'
        body = {'service_key': params['service_key'], 'country': params.get('country', 'CM')}
        if params.get('provider'):
            body['provider'] = params['provider']

        return ContactVerificationResponse(
            self.execute_request('POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(), body)
        )

    def get_pricing(self) -> PaymentAppResponse:
        """
        Get pricing metadata of the payment application.

        Returns:
            PaymentAppResponse
        """
        endpoint = 'payment/pricing/'

        return PaymentAppResponse(self.execute_request('GET', endpoint, datetime.now()))


class WalletOperation(AOperation):
    """
    Wallet operation class to interact with the MeSomb wallet service
    """
    service = 'wallet'

    def __init__(self, provider_key, access_key, secret_key):
        super().__init__(provider_key, access_key, secret_key)

    def create_wallet(self, **params: Unpack[WalletCreateParams]):
        """
        Create a wallet in MeSomb

        Args:
            **params: Wallet creation parameters defined in ``WalletCreateParams``.

        Returns:
            Wallet
        """
        endpoint = 'wallet/wallets/'

        body = {
            'last_name': params['last_name'],
            'phone_number': params['phone_number'],
            'gender': params['gender'],
            'country': params.get('country', 'CM'),
        }

        if params.get('first_name'):
            body['first_name'] = params['first_name']

        if params.get('email'):
            body['email'] = params['email']

        if params.get('number'):
            body['number'] = params['number']

        return Wallet(self.execute_request('POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(), body))

    def update_wallet(self, identifier: int, **params: Unpack[WalletUpdateParams]):
        """
        Update a wallet in MeSomb.

        Args:
            identifier: the identifier of the wallet
            **params: Wallet update parameters defined in ``WalletUpdateParams``.

        Returns:
            Wallet
        """

        endpoint = f'wallet/wallets/{identifier}/'

        body = {
            'last_name': params['last_name'],
            'phone_number': params['phone_number'],
            'gender': params['gender'],
            'country': params.get('country', 'CM'),
        }

        if params.get('first_name'):
            body['first_name'] = params['first_name']

        if params.get('email'):
            body['email'] = params['email']

        return Wallet(self.execute_request('PUT', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(), body))

    def get_wallet(self, identifier: int):
        """
        Get a wallet in MeSomb

        Args:
            identifier (int): the identifier of the wallet

        Returns:
            Wallet
        """
        endpoint = f'wallet/wallets/{identifier}/'

        return Wallet(self.execute_request('GET', endpoint, datetime.now()))

    def delete_wallet(self, identifier: int):
        """
        Delete a wallet in MeSomb

        Args:
            identifier (int): the identifier of the wallet

        Returns:
            None
        """
        endpoint = f'wallet/wallets/{identifier}/'

        return self.execute_request('DELETE', endpoint, datetime.now())

    def add_money(self, wallet: int, **params: Unpack[WalletAddMoneyParams]) -> WalletTransaction:
        """
        Add money to a wallet

        Args:
            wallet: the identifier of the wallet
            **params: Wallet credit parameters defined in ``WalletAddMoneyParams``.

        Returns:
            WalletTransaction
        """

        endpoint = f'wallet/wallets/{wallet}/adjust/'

        data = {'amount': params['amount'], 'direction': 1}

        if params.get('message'):
            data['message'] = params['message']

        if params.get('external_id'):
            data['trxID'] = params['external_id']

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def remove_money(self, wallet: int, **params: Unpack[WalletRemoveMoneyParams]) -> WalletTransaction:
        """
        Remove money from a wallet

        Args:
            wallet: the identifier of the wallet
            **params: Wallet debit parameters defined in ``WalletRemoveMoneyParams``.

        Returns:
            WalletTransaction
        """
        endpoint = f'wallet/wallets/{wallet}/adjust/'

        data = {'amount': params['amount'], 'direction': -1, 'force': params.get('force', False)}

        if params.get('message'):
            data['message'] = params['message']

        if params.get('external_id'):
            data['trxID'] = params['external_id']

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def transfert_money(self, source: int, dest: int, **params: Unpack[WalletTransferMoneyParams]) -> WalletTransaction:
        """
        Transfer money from a wallet to another

        Args:
            source: the identifier of the source wallet
            dest: the identifier of the destination wallet
            **params: Transfer parameters defined in ``WalletTransferMoneyParams``.

        Returns:
            WalletTransaction
        """
        endpoint = f'wallet/wallets/{source}/transfer/'

        data = {'amount': params['amount'], 'destination': dest, 'force': params.get('force', False)}

        if params.get('message'):
            data['message'] = params['message']

        if params.get('external_id'):
            data['trxID'] = params['external_id']

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def get_wallets(self, page=1):
        """
        Get wallets paginated

        Args:
            page: the page number (Default value = 1)

        Returns:
            PaginatedWallets
        """
        endpoint = f'wallet/wallets/?page={page}'

        return PaginatedWallets(self.execute_request('GET', endpoint, datetime.now()))

    def get_transaction(self, identifier: int):
        """
        Get a transaction in MeSomb

        Args:
            identifier (int): the identifier of the transaction

        Returns:
            WalletTransaction
        """
        endpoint = f'wallet/transactions/{identifier}/'

        return WalletTransaction(self.execute_request('GET', endpoint, datetime.now()))

    def list_transactions(self, page: int = 1, wallet: Optional[int] = None):
        """
        Listing transactions from MeSomb

        Args:
            page (int): the page number (Default value = 1)
            wallet (int, optional): the identifier of the wallet (Default value = None)

        Returns:
            PaginatedWalletTransactions
        """
        endpoint = f'wallet/transactions/?page={page}'

        if wallet:
            endpoint += f'&wallet={wallet}'

        return PaginatedWalletTransactions(self.execute_request('GET', endpoint, datetime.now()))

    def get_transactions(self, ids, source='MESOMB') -> List[WalletTransaction]:
        """
        Get transactions base on external in MeSomb's IDs

        Args:
            ids: list of ids
            source: source of transactions ids MESOMB or EXTERNAL

        Returns:
            List[WalletTransaction]
        """
        endpoint = f"wallet/transactions/search/?{'&'.join([f'ids={id}' for id in ids])}&source={source}"

        return [WalletTransaction(t) for t in self.execute_request('GET', endpoint, datetime.now())]


class FundraisingOperation(AOperation):
    """
    Fundraising operation class to interact with the MeSomb fundraising service
    """
    service = 'fundraising'

    def make_contribution(self, **params: Unpack[FundraisingContributionParams]) -> ContributionResponse:
        """
        Make a contribution to a fundraising campaign

        Args:
            **params: Contribution parameters defined in ``FundraisingContributionParams``.

        Returns:
            ContributionResponse

        """
        assert params['amount'] > 0, 'Amount must be greater than 0'
        if not params.get('anonymous', False):
            assert params.get('full_name'), 'Full name is required'
            assert params.get('contact'), 'Contact is required'

        endpoint = 'fundraising/contribute/'

        currency = params.get('currency', 'XAF')
        body = {
            'amount': params['amount'],
            'payer': params['payer'],
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': currency,
            'amount_currency': currency,
            'conversion': params.get('conversion', False),
            'anonymous': params.get('anonymous', False),
            'accept_terms': params.get('accept_terms', True),
        }

        if params.get('trx_id'):
            body['trxID'] = params['trx_id']

        if params.get('location'):
            body['location'] = params['location']

        if params.get('contact'):
            body['contact'] = params['contact']

        if params.get('full_name'):
            body['full_name'] = params['full_name']

        if params.get('line_items'):
            body['line_items'] = params['line_items']

        return ContributionResponse(
            self.execute_request(
                'POST', endpoint, datetime.now(), params.get('nonce') or RandomGenerator.nonce(),
                body, params.get('mode', 'synchronous')
            )
        )

    def get_contributions(self, ids, source='MESOMB') -> List[Contribution]:
        """
        Get contributions from MeSomb by IDs.

        Args:
            source: source of the contributionID: MESOMB or EXTERNAL (Default value = 'MESOMB')
            ids: list of ids

        Returns:
            List[Contribution]
        """
        assert source in ['MESOMB', 'EXTERNAL'], 'Source must be MESOMB or EXTERNAL'

        endpoint = f"fundraising/contributions/?ids={','.join(ids)}&source={source}"

        return [Contribution(item) for item in self.execute_request('GET', endpoint, datetime.now())]

    def check_contributions(self, ids, source='MESOMB') -> List[Contribution]:
        """
        Check contributions from MeSomb by IDs.

        Args:
            source: source of the contributionID: MESOMB or EXTERNAL (Default value = 'MESOMB')
            ids: list of ids

        Returns:
            List[Contribution]
        """

        assert source in ['MESOMB', 'EXTERNAL'], 'Source must be MESOMB or EXTERNAL'

        endpoint = f"fundraising/contributions/check/?ids={','.join(ids)}&source={source}"
        return [Contribution(item) for item in self.execute_request('GET', endpoint, datetime.now())]


class CustomerOperation(AOperation):
    service = 'payment'

    def __init__(self, access_key, secret_key, language='en'):
        super().__init__(None, access_key, secret_key, language=language)

    def list(self, page: int = 1) -> PaginatedCustomers:
        """
        Get customers paginated.

        Args:
            page (int): the page number (Default value = 1)

        Returns:
            PaginatedCustomers
        """
        endpoint = f'customers/?page={page}'

        return PaginatedCustomers(self.execute_request('GET', endpoint, datetime.now()))

    def create(self, **params: Unpack[CustomerParams]) -> Customer:
        """
        Create a customer for the current application.

        Args:
            **params: Customer creation parameters defined in ``CustomerParams``.

        Returns:
            Customer
        """
        endpoint = 'customers/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Customer(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def get(self, identifier: int) -> Customer:
        """
        Retrieve a customer created by the current application.

        Args:
            identifier (int): the identifier of the customer

        Returns:
            Customer
        """
        endpoint = f'customers/{identifier}/'

        return Customer(self.execute_request('GET', endpoint, datetime.now()))

    def update(self, identifier: int, **params: Unpack[CustomerParams]) -> Customer:
        """
        Update a customer created by the current application.

        Args:
            identifier (int): the identifier of the customer
            **params: Customer update parameters defined in ``CustomerParams``.

        Returns:
            Customer
        """
        endpoint = f'customers/{identifier}/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Customer(
            self.execute_request('PUT', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def patch(self, identifier: int, **params: Unpack[CustomerParams]) -> Customer:
        """
        Partially update a customer created by the current application.

        Args:
            identifier (int): the identifier of the customer
            **params: Customer patch parameters defined in ``CustomerParams``.

        Returns:
            Customer
        """
        endpoint = f'customers/{identifier}/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Customer(
            self.execute_request('PATCH', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def delete(self, identifier: int):
        """
        Delete a customer created by the current application.

        Args:
            identifier (int): the identifier of the customer

        Returns:
            None
        """
        endpoint = f'customers/{identifier}/'

        return self.execute_request('DELETE', endpoint, datetime.now())


class ProductOperation(AOperation):
    service = 'payment'

    def __init__(self, access_key, secret_key, language='en'):
        super().__init__(None, access_key, secret_key, language=language)

    def list(self, page: int = 1) -> PaginatedProducts:
        """
        Get products paginated.

        Args:
            page (int): the page number (Default value = 1)

        Returns:
            PaginatedProducts
        """
        endpoint = f'products/?page={page}'

        return PaginatedProducts(self.execute_request('GET', endpoint, datetime.now()))

    def create(self, **params: Unpack[ProductCreateParams]) -> Product:
        """
        Create a product for the current application.

        Args:
            **params: Product creation parameters defined in ``ProductCreateParams``.

        Returns:
            Product
        """
        endpoint = 'products/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Product(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def get(self, identifier: str) -> Product:
        """
        Retrieve a product created by the current application.

        Args:
            identifier (str): the identifier of the product

        Returns:
            Product
        """
        endpoint = f'products/{identifier}/'

        return Product(self.execute_request('GET', endpoint, datetime.now()))

    def update(self, identifier: str, **params: Unpack[ProductUpdateParams]) -> Product:
        """
        Update a product created by the current application.

        Args:
            identifier (str): the identifier of the product
            **params: Product update parameters defined in ``ProductUpdateParams``.

        Returns:
            Product
        """
        endpoint = f'products/{identifier}/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Product(
            self.execute_request('PUT', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def patch(self, identifier: str, **params: Unpack[ProductPatchParams]) -> Product:
        """
        Partially update a product created by the current application.

        Args:
            identifier (str): the identifier of the product
            **params: Product patch parameters defined in ``ProductPatchParams``.

        Returns:
            Product
        """
        endpoint = f'products/{identifier}/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}

        return Product(
            self.execute_request('PATCH', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def delete(self, identifier: str):
        """
        Delete a product created by the current application.

        Args:
            identifier (str): the identifier of the product

        Returns:
            None
        """
        endpoint = f'products/{identifier}/'

        return self.execute_request('DELETE', endpoint, datetime.now())


class CheckOutOperation(AOperation):
    service = 'payment'

    def retreive(self, identifier: str) -> CheckoutSession:
        """
        Retrieve a checkout session by identifier.

        Args:
            identifier (str): the identifier of the checkout session

        Returns:
            CheckoutSession
        """
        endpoint = f'checkout/sessions/{identifier}/'

        return CheckoutSession(self.execute_request('GET', endpoint, datetime.now()))

    def create(self, **params: Unpack[CheckoutCreateParams]) -> CheckoutSession:
        """
        Create a checkout session.

        Args:
            **params: Checkout creation parameters defined in ``CheckoutCreateParams``.

        Returns:
            CheckoutSession
        """
        endpoint = 'checkout/sessions/'
        nonce = params.get('nonce')
        body = {k: v for k, v in params.items() if k != 'nonce' and v is not None}
        body.setdefault('mode', 'payment')
        body.setdefault('currency', 'XAF')

        return CheckoutSession(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body)
        )

    def expire(self, identifier: str) -> CheckoutSession:
        """
        Expire a checkout session.

        Args:
            identifier (str): the identifier of the checkout session

        Returns:
            CheckoutSession
        """
        endpoint = f'checkout/sessions/{identifier}/expire/'

        return CheckoutSession(self.execute_request('PATCH', endpoint, datetime.now()))

    def delete(self, identifier: str):
        """
        Delete a checkout session.

        Args:
            identifier (str): the identifier of the checkout session

        Returns:
            dict
        """
        endpoint = f'checkout/sessions/{identifier}/'

        return self.execute_request('DELETE', endpoint, datetime.now())
