import json
from datetime import datetime

import requests

from pymesomb import settings
from pymesomb.exceptions import ServiceNotFoundException, PermissionDeniedException, InvalidClientRequestException, \
  ServerException
from pymesomb.models import TransactionResponse, Application
from pymesomb.signature import Signature


class PaymentOperation:
  def __init__(self, application_key, access_key, secret_key):
    self.application_key = application_key
    self.access_key = access_key
    self.secret_key = secret_key

  def build_url(self, endpoint):
    return '{}/en/api/{}/{}'.format(settings.host, settings.api_version, endpoint)

  def get_authorization(self, method, endpoint, date, nonce, headers=None, body=None):
    if headers is None:
      headers = {}

    url = self.build_url(endpoint)

    credentials = {'access_key': self.access_key, 'secret_key': self.secret_key}

    return Signature.sign_request('payment', method, url, date, nonce, credentials, headers, body)

  def process_client_exception(self, response):
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

  def make_collect(self, amount, service, payer, date, nonce, country='CM', currency='XAF', fees_included=True,
                   mode='synchronous', conversion=False, location=None, customer=None, product=None, extra=None):
    """
    Collect money a use account
    [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

    :param amount: amount to collect
    :param service: MTN, ORANGE, AIRTEL
    :param payer: account number to collect from
    :param date: date of the request
    :param nonce: unique string on each request
    :param country: country CM, NE
    :param currency: code of the currency of the amount
    :param fees_included: if MeSomb fees is already included in the money you are collecting
    :param conversion: In case of foreign currently defined if you want to rely on MeSomb to convert the amount in the local currency
    :param mode: asynchronous or synchronous
    :param location: dict containing the location of the customer check the documentation
    :param customer: dict containing information of the customer check the documentation
    :param product: dict containing information of the product check the documentation
    :param extra: Extra parameter to send in the body check the API documentation
    :return: request response
    """

    endpoint = 'payment/collect/'
    url = self.build_url(endpoint)

    body = {
      'amount': amount,
      'payer': payer,
      'fees': fees_included,
      'service': service,
      'country': country,
      'currency': currency,
      'conversion': conversion
    }
    if extra is not None:
      body.update(extra)

    if location is not None:
      body['location'] = location

    if customer is not None:
      body['customer'] = customer

    if product is not None:
      body['product'] = product

    authorization = self.get_authorization('POST', endpoint, date, nonce, headers={'content-type': 'application/json'},
                                           body=body)

    headers = {
      'x-mesomb-date': str(int(date.timestamp())),
      'x-mesomb-nonce': nonce,
      'Authorization': authorization,
      'X-MeSomb-Application': self.application_key,
      'X-MeSomb-OperationMode': mode,
    }

    response = requests.post(url, json=body, headers=headers)
    status_code = response.status_code
    if status_code >= 400:
      self.process_client_exception(response)

    return TransactionResponse(response.json())

  def make_deposit(self, amount, service, receiver, date, nonce=None, country='CM', currency='XAF', extra=None):
    """
    Method to make deposit in a receiver mobile account.
    [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

    :param amount: the amount of the transaction
    :param service: service code (MTN, ORANGE, AIRTEL, ...)
    :param receiver: receiver account (in the local phone number)
    :param date: datetime of the request
    :param nonce: Unique key generated for each transaction
    :param country: country code 'CM' by default
    :param currency: currency of the transaction (XAF, XOF, ...) XAF by default
    :param extra: Extra parameter to send in the body check the API documentation
    :return: request response
    """
    endpoint = 'payment/deposit/'
    url = self.build_url(endpoint)

    body = {
      'amount': amount,
      'receiver': receiver,
      'service': service,
      'country': country,
      'currency': currency,
    }
    if extra is not None:
      body.update(extra)

    authorization = self.get_authorization('POST', endpoint, date, nonce, headers={'content-type': 'application/json'},
                                           body=body)

    headers = {
      'x-mesomb-date': str(int(date.timestamp())),
      'x-mesomb-nonce': nonce,
      'Authorization': authorization,
      'X-MeSomb-Application': self.application_key,
    }

    response = requests.post(url, json=body, headers=headers)

    status_code = response.status_code
    if status_code >= 400:
      self.process_client_exception(response)

    return TransactionResponse(response.json())

  def update_security(self, field, action, value=None, date=None):
    """
    Update security parameters of your service on MeSomb
    :param field: which security field you want to update (check API doucumentation)
    :param action: SET or UNSET
    :param value: value of the field
    :param date: date of the request
    :return: request
    """
    endpoint = 'payment/security/'
    url = self.build_url(endpoint)
    body = {'field': field, 'action': action}
    if value:
      body['value'] = value

    if date is None:
      date = datetime.now()

    authorization = self.get_authorization('POST', endpoint, date, '', headers={'content-type': 'application/json'},
                                           body=body)

    headers = {
      'x-mesomb-date': str(int(date.timestamp())),
      'x-mesomb-nonce': '',
      'Authorization': authorization,
      'X-MeSomb-Application': self.application_key,
    }

    response = requests.post(url, json=body, headers=headers)

    status_code = response.status_code
    if status_code >= 400:
      self.process_client_exception(response)

    return Application(response.json())

  def get_status(self, date=None):
    """
    Get the current status of your service on MeSomb

    :param date: date of the request
    :return:
    """
    endpoint = 'payment/status/'
    url = self.build_url(endpoint)

    if date is None:
      date = datetime.now()

    headers = {
      'x-mesomb-date': str(int(date.timestamp())),
      'x-mesomb-nonce': '',
      'Authorization': self.get_authorization('GET', endpoint, date, ''),
      'X-MeSomb-Application': self.application_key,
    }

    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code >= 400:
      self.process_client_exception(response)

    return Application(response.json())

  def get_transactions(self, ids, date=None):
    """
    Get transactions from MeSomb by IDs.

    :param date: date of the request
    :param ids: list of ids
    :return: request response
    """
    endpoint = 'payment/transactions/?ids={}'.format(','.join(ids))
    url = self.build_url(endpoint)

    if date is None:
      date = datetime.now()

    headers = {
      'x-mesomb-date': str(int(date.timestamp())),
      'x-mesomb-nonce': '',
      'Authorization': self.get_authorization('GET', endpoint, date, ''),
      'X-MeSomb-Application': self.application_key,
    }

    response = requests.get(url, headers=headers)

    status_code = response.status_code
    if status_code >= 400:
      self.process_client_exception(response)

    return response.json()
