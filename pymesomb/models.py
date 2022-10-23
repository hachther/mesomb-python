class TransactionResponse:
  def __init__(self, data):
    self.success = data['success']
    self.message = data['message']
    self.redirect = data['redirect']
    self.data = data['transaction']
    self.reference = data['reference']
    self.status = data['status']

  def __str__(self):
    return self.data['id']

  def is_operation_success(self):
    return self.success

  def is_transaction_success(self):
    return self.success and self.status == 'SUCCESS'


class Application:
  def __init__(self, data):
    self.key = data['key']
    self.logo = data['logo']
    self.balances = data['balances']
    self.countries = data['countries']
    self.description = data['description']
    self.isLive = data['is_live']
    self.name = data['name']
    self.security = data['security']
    self.status = data['status']
    self.url = data['url']

  def get_security_field(self, field):
    return self.security.get(field, None)