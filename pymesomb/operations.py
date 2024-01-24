import json
from datetime import datetime

import requests

from pymesomb import mesomb
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException, \
    ServerException
from pymesomb.models import TransactionResponse, Application, Transaction
from pymesomb.signature import Signature


def process_client_exception(response):
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


def build_url(endpoint):
    return '{}/en/api/{}/{}'.format(mesomb.host, mesomb.api_version, endpoint)


class PaymentOperation:
    def __init__(self, application_key, access_key, secret_key):
        self.application_key = application_key
        self.access_key = access_key
        self.secret_key = secret_key

    def get_authorization(self, method, endpoint, date, nonce, headers=None, body=None):
        if headers is None:
            headers = {}

        url = build_url(endpoint)

        credentials = {'access_key': self.access_key, 'secret_key': self.secret_key}

        return Signature.sign_request('payment', method, url, date, nonce, credentials, headers, body)

    def _execute_request(self, method, endpoint, date, nonce='', body=None, mode=None):
        url = build_url(endpoint)

        headers = {
            'x-mesomb-date': str(int(date.timestamp())),
            'x-mesomb-nonce': nonce,
            'X-MeSomb-Application': self.application_key,
        }
        if body:
            body['source'] = 'PyMeSomb/{}'.format(mesomb.version)
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
            process_client_exception(response)

        return response.json()

    def make_collect(self, params):
        """
        Collect money a use account
        [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

        :param params: dict with the below information
            - amount: amount to collect
            - service: payment service with the possible values MTN, ORANGE, AIRTEL
            - payer: account number to collect from
            - date: date of the request
            - nonce: unique string on each request
            - country: 2 letters country code of the service (configured during your service registration in MeSomb)
            - currency: currency of your service depending on your country
            - fees: false if your want MeSomb fees to be computed and included in the amount to collect
            - mode: asynchronous or synchronous
            - conversion: true in case of foreign currently defined if you want to rely on MeSomb to convert the amount in the local currency
            - location: Map containing the location of the customer with the following attributes: town, region and location all string.
            - products: It is array of products. Each product are Map with the following attributes: name string, category string, quantity int and amount float
            - customer: a Map containing information about the customer: phone string, email: string, first_name string, last_name string, address string, town string, region string and country string
            - trxID: if you want to include your transaction ID in the request
            - extra: Map to add some extra attribute depending on the API documentation
        :return: TransactionResponse
        """

        endpoint = 'payment/collect/'

        body = {
            'amount': params['amount'],
            'payer': params['payer'],
            'fees': params.get('fees', True),
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
            'conversion': params.get('conversion', False)
        }
        if 'trxID' in params:
            body['trxID'] = params['trxID']

        if 'extra' in params:
            body.update(params['extra'])

        if 'location' in params:
            body['location'] = params['location']

        if 'customer' in params:
            body['customer'] = params['customer']

        if 'products' in params:
            body['products'] = params['products']

        date = params.get('date', datetime.now())
        nonce = params.get('nonce')

        return TransactionResponse(
            self._execute_request('POST', endpoint, date, nonce, body, params.get('mode', 'synchronous')))

    def make_deposit(self, params):
        """
        Method to make deposit in a receiver mobile account.
        [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

        :param params: dict with the below information
            - amount: amount to collect
            - service: payment service with the possible values MTN, ORANGE, AIRTEL
            - receiver: account number to depose money
            - date: date of the request
            - nonce: unique string on each request
            - country: 2 letters country code of the service (configured during your service registration in MeSomb)
            - currency: currency of your service depending on your country
            - fees: false if your want MeSomb fees to be computed and included in the amount to collect
            - conversion: true in case of foreign currently defined if you want to rely on MeSomb to convert the amount in the local currency
            - location: Map containing the location of the customer with the following attributes: town, region and location all string.
            - products: It is array of products. Each product are Map with the following attributes: name string, category string, quantity int and amount float
            - customer: a Map containing information about the customer: phone string, email: string, first_name string, last_name string, address string, town string, region string and country string
            - trxID: if you want to include your transaction ID in the request
            - extra: Map to add some extra attribute depending on the API documentation
        :return: TransactionResponse
        """
        endpoint = 'payment/deposit/'
        url = build_url(endpoint)

        body = {
            'amount': params['amount'],
            'receiver': params['receiver'],
            'service': params['service'],
            'country': params.get('country', 'CM'),
            'currency': params.get('currency', 'XAF'),
        }

        if 'extra' in params:
            body.update(params['extra'])

        if 'trxID' in params:
            body['trxID'] = params['trxID']

        if 'location' in params:
            body['location'] = params['location']

        if 'customer' in params:
            body['customer'] = params['customer']

        if 'products' in params:
            body['products'] = params['products']

        date = params.get('date', datetime.now())
        nonce = params['nonce']

        return TransactionResponse(self._execute_request('POST', endpoint, date, nonce, body))

    def update_security(self, field, action, value=None, date=None):
        """
        Update security parameters of your service on MeSomb
        :param field: which security field you want to update (check API doucumentation)
        :param action: SET or UNSET
        :param value: value of the field
        :param date: date of the request
        :return: Application
        """
        endpoint = 'payment/security/'
        body = {'field': field, 'action': action}
        if value:
            body['value'] = value

        if date is None:
            date = datetime.now()

        return Application(self._execute_request('POST', endpoint, date, body=body))

    def get_status(self):
        """
        Get the current status of your service on MeSomb

        :param date: date of the request
        :return: Application
        """
        endpoint = 'payment/status/'

        return Application(self._execute_request('GET', endpoint, datetime.now()))

    def get_transactions(self, ids, source='MESOMB'):
        """
        Get transactions from MeSomb by IDs.

        :param source: source of the transactionID
        :param ids: list of ids
        :return: list of Transaction
        """
        endpoint = 'payment/transactions/?ids={}&source={}'.format(','.join(ids), source)

        return [Transaction(item) for item in self._execute_request('GET', endpoint, datetime.now())]

    def check_transactions(self, ids, source='MESOMB'):
        """
        Get transactions from MeSomb by IDs.

        :param source: source of the transactionID
        :param ids: list of ids
        :return: list of Transaction
        """
        endpoint = 'payment/transactions/check/?ids={}&source={}'.format(','.join(ids), source)
        return [Transaction(item) for item in self._execute_request('GET', endpoint, datetime.now())]
