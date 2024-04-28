class Location:
    def __init__(self, data):
        self.town = data.get('town')
        self.region = data.get('region')
        self.country = data.get('country')


class Customer:
    def __init__(self, data):
        self.email = data.get('email', None)
        self.phone = data.get('phone', None)
        self.town = data.get('town', None)
        self.region = data.get('region', None)
        self.country = data.get('country', None)
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        self.address = data.get('address', None)


class Product:
    def __init__(self, data):
        self.name = data['name']
        self.category = data.get('category', 'category')
        self.quantity = data.get('quantity', None)
        self.amount = data.get('amount', None)


class Transaction:
    def __init__(self, data):
        self.pk = data['pk']
        self.status = data['status']
        self.type = data['type']
        self.amount = data['amount']
        self.fees = data['fees']
        self.b_party = data['b_party']
        if 'message' in data:
            self.message = data['message']
        self.service = data['service']
        if 'reference' in data:
            self.reference = data['reference']
        self.ts = data['ts']
        self.country = data['country']
        self.currency = data['currency']
        if 'fin_trx_id' in data:
            self.fin_trx_id = data['fin_trx_id']
        if 'trxamount' in data:
            self.trxamount = data['trxamount']
        if data.get('location'):
            self.location = Location(data['location'])
        if data.get('customer'):
            self.customer = Customer(data['customer'])
        if data.get('products'):
            self.products = [Product(p) for p in data['products']]
        # self.products = data['products?.map((d: Record < string, any >) = > new Product(d))']

    def __str__(self):
        return self.pk


class TransactionResponse:
    def __init__(self, data):
        self.raw_response = data

        self.success = data['success']
        self.message = data['message']
        self.redirect = data['redirect']
        self.transaction = Transaction(data['transaction'])
        self.reference = data['reference']
        self.status = data['status']

    def __str__(self):
        return '{}: {}'.format(self.status, self.message)

    def is_operation_success(self):
        return self.success

    def is_transaction_success(self):
        return self.success and self.transaction.status == 'SUCCESS'


class ApplicationBalance:
    def __init__(self, data):
        self.country = data.get("country")
        self.currency = data.get("currency")
        self.provider = data.get("provider")
        self.value = data.get("value")
        self.service_name = data.get("service_name")


class Application:
    def __init__(self, data):
        self.key = data['key']
        self.logo = data['logo']
        self.balances = [ApplicationBalance(b) for b in data['balances']]
        self.countries = data['countries']
        self.description = data['description']
        self.isLive = data['is_live']
        self.name = data['name']
        self.security = data['security']
        self.status = data['status']
        self.url = data['url']

    def get_security_field(self, field):
        return self.security.get(field, None)

    def get_balance(self, country=None, service=None):
        balance = 0
        for bal in self.balances:
            if country and bal.country != country:
                continue
            if service and bal.provider != service:
                continue
            balance += bal.value
        return balance
