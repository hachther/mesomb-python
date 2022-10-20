import requests

from pymesomb.settings import algorithm, host, api_version
from pymesomb.signature import sign_request


def make_deposit(configs, amount, service, receiver, date, country='CM', currency='XAF', nonce=None, extra=None):
  '''
  Method to make deposit in a receiver mobile account.
  [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

  :param configs: dictionary containing application_id, secret_key, access_key
  :param amount: the amount of the transaction
  :param service: service code (MTN, ORANGE, AIRTEL, ...)
  :param receiver: receiver account (in the local phone number)
  :param date: datetime of the request
  :param country: country code 'CM', 'NE' by default
  :param currency: currency of the transaction (XAF, XOF, ...) XAF by default
  :param nonce: Unique key generated for each transaction
  :param extra: Extra parameter to send in the body check the API documentation
  :return: request response
  '''
  application_key = configs['application_key']
  url = '{}/en/api/{}/payment/deposit/'.format(host, api_version)
  if extra is None:
    extra = {}

  payload = {
    'amount': amount,
    'message': 'Hello word',
    'receiver': receiver,
    'reference': 'DepositI',
    'service': service,
    'country': country,
    'currency': currency,
  }
  payload.update(extra)

  authorization = sign_request('payment', 'POST', url, date, nonce,
                               {'secret_key': configs['secret_key'], 'access_key': configs['access_key']},
                               headers={'content-type': 'application/json'},
                               body=payload)

  headers = {
    'x-mesomb-date': str(int(date.timestamp())),
    'x-mesomb-nonce': nonce,
    'Authorization': authorization,
    'X-MeSomb-Application': application_key,
  }

  return requests.post(url, json=payload, headers=headers)


def make_payment(configs, amount, service, payer, date, country='CM', currency='XAF', include_fees=True,
                 conversion=False, nonce=None, mode='synchronous', location=None, customer=None, product=None, extra=None):
  '''
  [Check the documentation here](https://mesomb.hachther.com/en/api/schema/)

  :param configs: dictionary containing application_id, secret_key, access_key
  :param amount: amount to collect
  :param service: MTN, ORANGE, AIRTEL
  :param payer: account number to collect from
  :param date: date of the request
  :param country: country CM, NE
  :param currency: code of the currency of the amount
  :param include_fees: if your want MeSomb to include and compute fees in the amount to collect
  :param conversion: In case of foreign currently defined if you want to rely on MeSomb to convert the amount in the local currency
  :param nonce: unique string on each request
  :param mode: asynchronous or synchronous
  :param location: dict containing the location of the customer check the documentation
  :param customer: dict containing information of the customer check the documentation
  :param product: dict containing information of the product check the documentation
  :param extra: Extra parameter to send in the body check the API documentation
  :return: request response
  '''
  application_key = configs['application_key']
  url = '{}/en/api/v1.1/payment/collect/'.format(host, api_version)

  payload = {
    'amount': amount,
    'payer': payer,
    'fees': include_fees,
    'service': service,
    'country': country,
    'currency': currency,
    'conversion': conversion
  }
  if extra is not None:
    payload.update(extra)

  if location is not None:
    payload['location'] = location

  if customer is not None:
    payload['customer'] = customer

  if product is not None:
    payload['product'] = product

  authorization = sign_request('payment', 'POST', url, date, nonce,
                               {'secret_key': configs['secret_key'], 'access_key': configs['access_key']},
                               headers={'content-type': 'application/json'},
                               body=payload)

  headers = {
    'x-mesomb-date': str(int(date.timestamp())),
    'x-mesomb-nonce': nonce,
    'Authorization': authorization,
    'X-MeSomb-Application': application_key,
    'X-MeSomb-OperationMode': mode,
  }

  return requests.post(url, json=payload, headers=headers)


def update_security(configs, field, action, value, date):
  '''
  Update security parameters of your service on MeSomb
  :param configs: dictionary containing application_id, secret_key, access_key
  :param field: which security field you want to update (check API doucumentation)
  :param action: SET or UNSET
  :param value: value of the field
  :param date: date of the request
  :return: request
  '''
  application_key = configs['application_key']
  url = '{}/en/api/{}/payment/security/'.format(host, api_version)
  payload = {'field': field, 'action': action, 'value': value}

  authorization = sign_request('payment', 'POST', url, date, '',
                               {'secret_key': configs['secret_key'], 'access_key': configs['access_key']},
                               headers={'content-type': 'application/json'},
                               body=payload)
  headers = {
    'x-mesomb-date': str(int(date.timestamp())),
    'x-mesomb-nonce': '',
    'Authorization': authorization,
    'X-MeSomb-Application': application_key,
  }

  return requests.post(url, json=payload, headers=headers)


def get_status(configs, date):
  '''
  Get the current status of your service on mesomb

  :param configs: dictionary containing application_id, secret_key, access_key
  :param date: date of the request
  :return:
  '''
  application_key = configs['application_key']
  url = '{}/en/api/{}/payment/status/'.format(host, api_version)

  authorization = sign_request('payment', 'GET', url, date, '',
                               {'secret_key': configs['secret_key'], 'access_key': configs['access_key']})
  headers = {
    'x-mesomb-date': str(int(date.timestamp())),
    'x-mesomb-nonce': '',
    'Authorization': authorization,
    'X-MeSomb-Application': application_key,
  }

  return requests.get(url, headers=headers)


def get_transactions(configs, date, ids):
  '''
  Get transactions from MeSomb by IDs.

  :param configs: dictionary containing application_id, secret_key, access_key
  :param date: date of the request
  :param ids: list of ids
  :return: request response
  '''
  application_key = configs['application_key']
  url = '{}/en/api/{}/payment/transactions/?ids={}'.format(host, api_version, ','.join(ids))

  authorization = sign_request('payment', 'GET', url, date, '',
                               {'secret_key': configs['secret_key'], 'access_key': configs['access_key']})

  headers = {
    'x-mesomb-date': str(int(date.timestamp())),
    'x-mesomb-nonce': '',
    'Authorization': authorization,
    'X-MeSomb-Application': application_key,
  }

  return requests.get(url, headers=headers)
