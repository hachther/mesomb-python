import json
from abc import ABC
from datetime import datetime
from typing import Optional, Dict, List, Any

import requests

from pymesomb import mesomb, __version__
from pymesomb.models import (TransactionResponse, Application, Transaction, Wallet, PaginatedWallets,
                             WalletTransaction, PaginatedWalletTransactions, ContributionResponse, Contribution)
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

        return response.json()


class PaymentOperation(AOperation):
    """
    Payment operation class to interact with the MeSomb payment service
    """
    service = 'payment'

    def __init__(self, application_key, access_key, secret_key):
        super().__init__(application_key, access_key, secret_key)

    def make_collect(self, amount: float, service: str, payer: str, nonce: Optional[str] = None, country: str = 'CM',
                     currency: str = 'XAF', fees: bool = True, mode: str = 'synchronous', conversion: bool = False,
                     location: Optional[Dict[str, str]] = None, products: Optional[List[Dict[str, str]]] = None,
                     customer: Optional[Dict[str, str]] = None, trx_id: Optional[str] = None) -> TransactionResponse:
        """Collect money a use account

        Args:
            amount (float): amount to collect
            service (str): payment service with the possible values MTN, ORANGE, AIRTEL
            payer (str): account number to collect money
            nonce (str, optional): unique string on each request
            country (str): 2 letters country code of the service, configured during your service registration
                        in MeSomb (Default value = 'CM')
            currency (str): currency of your service depending on your country (Default value = 'XAF')
            fees (bool): false if your want MeSomb fees to be computed and included in the amount to collect
                        (Default value = True)
            conversion (bool): true in case of foreign currently defined if you want to rely on MeSomb to convert
                        the amount in the local currency (Default value = False)
            location (dict): Map containing the location of the customer with the following attributes:
                        town, region and location all string.
            products (list): It is array of products. Each product are Map with the following attributes:
                        name string, category string, quantity int and amount float
            customer (dict): a Map containing information about the customer: phone string, email: string, first_name
                        string, last_name string, address string, town string, region string and country string
            trx_id (str): if you want to include your transaction ID in the request
            mode (str): Mode of the transaction synchronous or asynchronous (Default value = 'synchronous')

        Returns:
            TransactionResponse
        """

        endpoint = 'payment/collect/'

        body = {
            'amount': amount,
            'payer': payer,
            'fees': fees,
            'service': service,
            'country': country,
            'currency': currency,
            'amount_currency': currency,
            'conversion': conversion
        }
        if trx_id:
            body['trxID'] = trx_id

        if location:
            body['location'] = location

        if customer:
            body['customer'] = customer

        if products:
            body['products'] = products

        return TransactionResponse(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body, mode))

    def make_deposit(self, amount: float, service: str, receiver: str, nonce: Optional[str] = None,
                     country: Optional[str] = 'CM', currency: Optional[str] = 'XAF', conversion: Optional[bool] = False,
                     location: Optional[Dict[str, str]] = None, products: Optional[List[Dict[str, str]]] = None,
                     customer: Optional[Dict[str, str]] = None, trx_id: Optional[str] = None) -> TransactionResponse:
        """
        Method to make deposit in a receiver mobile account.

        Args:
            amount (float): amount to collect
            service (str): payment service with the possible values MTN, ORANGE, AIRTEL
            receiver (str): account number to depose money
            nonce (str, optional): unique string on each request
            country (str, optional): 2 letters country code of the service configured during your service
                    registration in MeSomb (Default value = 'CM')
            currency (str, optional): currency of your service depending on your country (Default value = 'XAF')
            conversion (bool, optional): true in case of foreign currently defined if you want to rely on
                    MeSomb to convert the amount in the local currency (Default value = False)
            location (dict): Map containing the location of the customer with the following attributes:
                    town, region and location all string.
            products (list): It is array of products. Each product are Map with the following attributes:
                    name string, category string, quantity int and amount float
            customer (dict): a Map containing information about the customer: phone string, email: string,
                    first_name string, last_name string, address string, town string, region string and country string
            trx_id (str): if you want to include your transaction ID in the request

        Returns:
            TransactionResponse
        """
        endpoint = 'payment/deposit/'

        body = {
            'amount': amount,
            'receiver': receiver,
            'service': service,
            'country': country,
            'currency': currency,
            'amount_currency': currency,
            'conversion': conversion,
        }

        if trx_id:
            body['trxID'] = trx_id

        if location:
            body['location'] = location

        if customer:
            body['customer'] = customer

        if products:
            body['products'] = products

        return TransactionResponse(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body))

    def make_yango_refill(self, amount: float, service: str, payer: str, driver_id: str, nonce=None,
                          country: Optional[str] = 'CM', currency: Optional[str] = 'XAF',
                          mode: Optional[str] = 'synchronous', location: Optional[Dict[str, str]] = None,
                          customer: Optional[Dict[str, str]] = None,
                          trx_id: Optional[str] = None) -> TransactionResponse:
        """
        Method to refill a Yango account.

        Args:
            amount (float): amount to collect
            service (str): payment service with the possible values MTN, ORANGE, AIRTEL
            payer (str): account number to depose money
            driver_id (str): the driver ID
            nonce (str, optional): unique string on each request
            country (str): 2 letters country code of the service configured during your service registration in
                    MeSomb (Default value = 'CM')
            currency (str): currency of your service depending on your country (Default value = 'XAF')
            mode (str): Mode of the transaction synchronous or asynchronous (Default value = 'synchronous')
            location (dict): Map containing the location of the customer with the following attributes:
                    town, region and location all string.
            customer (dict): a Map containing information about the customer: phone string, email: string,
                    first_name string, last_name string, address string, town string, region string and country string
            trx_id (str): if you want to include your transaction ID in the request

        Returns:
          TransactionResponse

        """
        endpoint = 'payment/yango/refill/'

        body = {
            'amount': amount,
            'payer': payer,
            'service': service,
            'driver_id': driver_id,
            'country': country,
            'currency': currency,
            'amount_currency': currency,
        }

        if trx_id:
            body['trxID'] = trx_id

        if location:
            body['location'] = location

        if customer:
            body['customer'] = customer

        return TransactionResponse(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body, mode))

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

    def refund_transaction(self, trx_id: str, amount: Optional[float] = None, conversion: Optional[bool] = None,
                           currency: str = None) -> TransactionResponse:
        """
        Refund a transaction in MeSomb

        Args:
            trx_id: the transaction identifier
            amount: the amount to refund
            conversion: true if you want to rely on MeSomb to convert the amount in the local
                currency (Default value = None)
            currency: currency of your service depending on your country (Default value = None)
        Returns:
            TransactionResponse
        """
        endpoint = f'payment/refund/'

        body = {'id': trx_id}
        if amount:
            body['amount'] = amount
        if currency:
            body['currency'] = currency
            body['amount_currency'] = currency
        if conversion:
            body['conversion'] = conversion

        return TransactionResponse(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(),
                                                       body))


class WalletOperation(AOperation):
    """
    Wallet operation class to interact with the MeSomb wallet service
    """
    service = 'wallet'

    def __init__(self, provider_key, access_key, secret_key):
        super().__init__(provider_key, access_key, secret_key)

    def create_wallet(self, last_name: str, phone_number: str, gender: str, first_name: Optional[str] = None,
                      country: Optional[str] = 'CM', email: Optional[str] = None, nonce: Optional[str] = None,
                      number: Optional[str] = None):
        """
        Create a wallet in MeSomb

        Args:
            last_name (str): the last name of the wallet owner
            phone_number (str): the phone number of the wallet owner
            gender (str): the gender of the wallet owner
            first_name (str, optional): the first name of the wallet owner
            country (str, optional): the country of the wallet owner (Default value = 'CM')
            email (str, optional): the email of the wallet owner
            nonce (str, optional): the nonce of the request (Default value = None)
            number (str, optional): the unique numeric wallet identifier, if not set we will generate one for you

        Returns:
            Wallet
        """
        endpoint = 'wallet/wallets/'

        body = {
            'last_name': last_name,
            'phone_number': phone_number,
            'gender': gender,
            'country': country,
        }

        if first_name:
            body['first_name'] = first_name

        if email:
            body['email'] = email

        if number:
            body['number'] = number

        return Wallet(self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body))

    def update_wallet(self, identifier: int, last_name: str, phone_number: str, gender: str,
                      first_name: Optional[str] = None, country: Optional[str] = 'CM', email: Optional[str] = None,
                      nonce: Optional[str] = None):
        """
        Create a wallet in MeSomb

        Args:
            identifier: the identifier of the wallet
            last_name (str): the last name of the wallet owner
            phone_number (str): the phone number of the wallet owner
            gender (str): the gender of the wallet owner
            first_name (str, optional): the first name of the wallet owner
            country (str, optional): the country of the wallet owner (Default value = 'CM')
            email (str, optional): the email of the wallet owner
            nonce (str, optional): the nonce of the request (Default value = None)

        Returns:
            Wallet
        """

        endpoint = f'wallet/wallets/{identifier}/'

        body = {
            'last_name': last_name,
            'phone_number': phone_number,
            'gender': gender,
            'country': country,
        }

        if first_name:
            body['first_name'] = first_name

        if email:
            body['email'] = email

        return Wallet(self.execute_request('PUT', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body))

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

    def add_money(self, wallet: int, amount: float, message: Optional[str] = None, external_id: Optional[str] = None) -> WalletTransaction:
        """
        Add money to a wallet

        Args:
            wallet: the identifier of the wallet
            amount: the amount to add to the wallet
            message: the message to add to the transaction (Default value = None)

        Returns:
            Wallet
        """

        endpoint = f'wallet/wallets/{wallet}/adjust/'

        data = {'amount': amount, 'direction': 1}

        if message:
            data['message'] = message

        if external_id:
            data['trxID'] = external_id

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def remove_money(self, wallet: int, amount: float, force: Optional[bool] = False, message: Optional[str] = None, external_id: Optional[str] = None) -> WalletTransaction:
        """
        Remove money from a wallet

        Args:
            wallet: the identifier of the wallet
            amount: the amount to remove from the wallet
            force: to force the operation if balance is not enough (Default value = False)
            message: the message to add to the transaction (Default value = None)

        Returns:
            Wallet
        """
        endpoint = f'wallet/wallets/{wallet}/adjust/'

        data = {'amount': amount, 'direction': -1, 'force': force}

        if message:
            data['message'] = message

        if external_id:
            data['trxID'] = external_id

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def transfert_money(self, source: int, dest: int, amount: float,
                        force: Optional[bool] = False, message: Optional[str] = None, external_id: Optional[str] = None) -> WalletTransaction:
        """
        Transfer money from a wallet to another

        Args:
            source: the identifier of the source wallet
            dest: the identifier of the destination wallet
            amount: the amount to transfer
            force: to force the operation if balance is not enough (Default value = False)

        Returns:
            Wallet
        """
        endpoint = f'wallet/wallets/{source}/transfer/'

        data = {'amount': amount, 'destination': dest, 'force': force}

        if message:
            data['message'] = message

        if external_id:
            data['trxID'] = external_id

        return WalletTransaction(self.execute_request('POST', endpoint, datetime.now(), RandomGenerator.nonce(), data))

    def get_wallets(self, page=1):
        """
        Get wallets paginated

        Args:
            page: the page number (Default value = 1)

        Returns:
            PaginatedWallets
        """
        endpoint = f'wallet//wallets/?page={page}'

        return PaginatedWallets(self.execute_request('GET', endpoint, datetime.now()))

    def get_transaction(self, identifier: int):
        """
        Get a transaction in MeSomb

        Args:
            identifier (int): the identifier of the transaction

        Returns:
            Transaction
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
            List[WalletTransaction]
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

    def make_contribution(self, amount: float, service: str, payer: str, nonce: Optional[str] = None,
                          country: str = 'CM',currency: str = 'XAF', mode: str = 'synchronous',
                          conversion: bool = False, anonymous: bool = False, accept_terms: bool = True,
                          location: Optional[Dict[str, str]] = None, contact: Optional[Dict[str, str]] = None,
                          full_name: Optional[Dict[str, str]] = None,
                          trx_id: Optional[str] = None) -> ContributionResponse:
        """
        Make a contribution to a fundraising campaign

        Args:
            amount: amount to contribute
            service: payment service with the possible values MTN, ORANGE, AIRTEL
            payer: account number to contribute
            nonce: unique string on each request
            country: 2 letters country code of the service, configured during your service registration in MeSomb
            currency: currency of your service depending on your country
            conversion: true in case of foreign currently defined if you want to rely on MeSomb to
                convert the amount in the local currency
            anonymous: true if you want to contribute anonymously
            accept_terms: true if you accept the terms of the contribution
            location: Map containing the location of the customer with the following attributes:
                town, region and location all string.
            contact: a Map containing information about the customer: phone_number string, email: string
            full_name: a Map containing information about the customer: first_name string, last_name string
            trx_id: if you want to include your transaction ID in the request

        Returns:
            ContributionResponse

        """
        assert amount > 0, 'Amount must be greater than 0'
        if not anonymous:
            assert full_name, 'Full name is required'
            assert contact, 'Contact is required'

        endpoint = 'fundraising/contribute/'

        body = {
            'amount': amount,
            'payer': payer,
            'service': service,
            'country': country,
            'currency': currency,
            'amount_currency': currency,
            'conversion': conversion,
            'anonymous': anonymous,
            'accept_terms': accept_terms,
        }

        if trx_id:
            body['trxID'] = trx_id

        if location:
            body['location'] = location

        if contact:
            body['contact'] = contact

        if full_name:
            body['full_name'] = full_name

        return ContributionResponse(
            self.execute_request('POST', endpoint, datetime.now(), nonce or RandomGenerator.nonce(), body, mode))

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
