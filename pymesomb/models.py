from abc import ABC
from datetime import datetime
from typing import Optional, List, Any, Dict


class Location:
    """
    Represents the location of a customer.

    Args:
        data (dict): The location data.

    Attributes:
        town (str): The town of the customer.
        region (str, optional): The region of the customer.
        country (str, optional): The country of the customer.
    """

    def __init__(self, data):
        self.town: str = data.get('town')
        self.region: Optional[str] = data.get('region')
        self.country: Optional[str] = data.get('country')


class Customer:
    """
    Represents a customer.

    Args:
        data (dict): The customer data.

    Attributes:
        email (str, optional): The email of the customer.
        phone (str, optional): The phone number of the customer.
        town (str, optional): The town of the customer.
        region (str, optional): The region of the customer.
        country (str, optional): The country of the customer.
        first_name (str, optional): The first name of the customer.
        last_name (str): The last name of the customer.
        address (str, optional): The address of the customer.
    """

    def __init__(self, data):
        self.email: Optional[str] = data.get('email', None)
        self.phone: Optional[str] = data.get('phone', None)
        self.town: Optional[str] = data.get('town', None)
        self.region: Optional[str] = data.get('region', None)
        self.country: Optional[str] = data.get('country', None)
        self.first_name: Optional[str] = data.get('first_name', None)
        self.last_name: str = data['last_name']
        self.address: Optional[str] = data.get('address', None)


class Product:
    """
    Represents a product.

    Args:
        data (dict): The product data.

    Attributes:
        id (str): The identifier of the product.
        name (str): The name of the product.
        category (str, optional): The category of the product.
        quantity (int, optional): The quantity of the product.
        amount (float, optional): The amount of the product.
    """

    def __init__(self, data):
        self.id: str = data['id']
        self.name: str = data['name']
        self.category: Optional[str] = data.get('category', 'category')
        self.quantity: Optional[int] = data.get('quantity', None)
        self.amount: Optional[float] = data.get('amount', None)


class ATransaction(ABC):
    """
    Represents a transaction.

    Args:
        data (dict): The transaction data.

    Attributes:
        pk (str): The primary key of the transaction.
        status (str): The status of the transaction.
        type (str): The type of the transaction.
        amount (float): The amount of the transaction.
        fees (float, optional): The fees of the transaction.
        b_party (str): The b party of the transaction.
        message (str, optional): The message of the transaction.
        service (str): The service of the transaction.
        reference (str, optional): The reference of the transaction.
        date (datetime): The timestamp of the transaction.
        country (str): The country of the transaction.
        currency (str): The currency of the transaction.
        fin_trx_id (str, optional): The financial transaction ID of the transaction.
        trxamount (float, optional): The transaction amount.
        location (Location, optional): The location of the transaction.
    """

    def __init__(self, data: Dict[str, Any]):
        self.pk: str = data['pk']
        self.status: str = data['status']
        self.type: str = data['type']
        self.amount: float = data['amount']
        self.fees: Optional[float] = data.get('fees')
        self.b_party: str = data['b_party']
        self.message: Optional[str] = data.get('message')
        self.service: str = data['service']
        self.reference: Optional[str] = data.get('reference')
        self.date: datetime = datetime.strptime(data['ts'], '%Y-%m-%dT%H:%M:%SZ')
        self.country: str = data['country']
        self.currency: str = data['currency']
        self.fin_trx_id: Optional[str] = data.get('fin_trx_id')
        self.trxamount: Optional[float] = data.get('trxamount')
        self.location: Optional[Location] = Location(data['location']) if data.get('location') else None

    def is_success(self) -> bool:
        """
        Check if the transaction was successful.

        Returns:
            bool: True if the transaction was successful, False otherwise.
        """
        return self.status == 'SUCCESS'

    def is_pending(self) -> bool:
        """
        Check if the transaction is pending.

        Returns:
            bool: True if the transaction is pending, False otherwise.
        """
        return self.status == 'PENDING'

    def is_failed(self) -> bool:
        """
        Check if the transaction failed.

        Returns:
            bool: True if the transaction failed, False otherwise.
        """
        return self.status == 'FAILED'


class Transaction(ATransaction):
    """
    Represents a transaction.
    This class extends :ATransaction:. It adds more attributes to the transaction.

    Args:
        data (dict): The transaction data.

    Attributes:
        pk (str): The primary key of the transaction.
        status (str): The status of the transaction.
        type (str): The type of the transaction.
        amount (float): The amount of the transaction.
        fees (float, optional): The fees of the transaction.
        b_party (str): The b party of the transaction.
        message (str, optional): The message of the transaction.
        service (str): The service of the transaction.
        reference (str, optional): The reference of the transaction.
        date (datetime): The timestamp of the transaction.
        country (str): The country of the transaction.
        currency (str): The currency of the transaction.
        fin_trx_id (str, optional): The financial transaction ID of the transaction.
        trxamount (float, optional): The transaction amount.
        location (Location, optional): The location of the transaction.
        customer (Customer, optional): The customer of the transaction.
        products (List[Product], optional): The products of the transaction.
    """

    def __init__(self, data: dict):
        super().__init__(data)
        self.customer: Optional[Customer] = Customer(data['customer']) if data.get('customer') else None
        self.products: Optional[List[Product]] = [Product(p) for p in data.get('products', [])]
        # self.products = data['products?.map((d: Record < string, any >) = > new Product(d))']

    def __str__(self):
        return self.pk


class TransactionResponse:
    """
    Represents the response of a transactional operation.

    Args:
        data (dict): The response data from the server.

    Attributes:
        success (bool): Whether the operation was successful.
        message (str, optional): The message returned by the operation.
        redirect (str, optional): The URL to redirect the user to.
        transaction (Transaction): The transaction object.
        reference (str, optional): The reference of the transaction.
        status (str): The status of the transaction.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

        self.success: bool = data['success']
        self.message: Optional[str] = data['message']
        self.redirect: Optional[str] = data['redirect']
        self.transaction: Transaction = Transaction(data['transaction'])
        self.reference: Optional[str] = data['reference']
        self.status: str = data['status']

    def __str__(self):
        return '{}: {}'.format(self.status, self.message)

    def is_operation_success(self):
        """ """
        return self.success

    def is_transaction_success(self):
        """ """
        return self.transaction.is_success()

    def get_data(self) -> Dict[str, Any]:
        return self._data


class ApplicationBalance:
    """ """

    def __init__(self, data):
        self.country = data.get("country")
        self.currency = data.get("currency")
        self.provider = data.get("provider")
        self.value = data.get("value")
        self.service_name = data.get("service_name")


class Application:
    """
    Represents an application.

    Args:
        data (dict): The application data.

    Attributes:
        key (str): The key of the application.
        logo (str, optional): The logo of the application.
        balances (List[ApplicationBalance]): The balances of the application.
        countries (List[str]): The countries supported by the application.
        description (str, optional): The description of the application.
        name (str): The name of the application.
        security (dict, optional): The security of the application.
        url (str, optional): The URL of the application
    """

    def __init__(self, data: Dict[str, Any]):
        self.key: str = data['key']
        self.logo: Optional[str] = data.get('logo')
        self.balances: List[ApplicationBalance] = [ApplicationBalance(b) for b in data['balances']]
        self.countries: List[str] = data['countries']
        self.description: Optional[str] = data.get('description')
        self.name: str = data['name']
        self.security: Optional[Dict[str, Any]] = data.get('security')
        self.url: Optional[str] = data.get('url')

    def get_balance(self, country=None, service=None):
        """

        Args:
          country:  (Default value = None)
          service:  (Default value = None)

        Returns:

        """
        balance = 0
        for bal in self.balances:
            if country and bal.country != country:
                continue
            if service and bal.provider != service:
                continue
            balance += bal.value
        return balance


class WalletTransaction:
    """
    Represents a wallet transaction.

    Args:
        data (dict): The transaction data.

    Attributes:
        id (int): The identifier of the transaction.
        status (str): The status of the transaction.
        type (str): The type of the transaction.
        amount (float): The amount of the transaction.
        direction (int): The direction of the transaction.
        wallet (int): The wallet identifier.
        balance_after (float, optional): The balance after the transaction.
        date (datetime): The date of the transaction.
        country (str): The country of the transaction.
        fin_trx_id (str): The financial transaction ID.
    """

    def __init__(self, data: Dict[str, Any]):
        self.id: int = data['id']
        self.status: str = data['status']
        self.type: str = data['type']
        self.amount: float = data['amount']
        self.direction: int = data['direction']
        self.wallet: int = data['wallet']
        self.balance_after: Optional[float] = data.get('balance_after')
        self.date: datetime = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        self.country: str = data['country']
        self.fin_trx_id: str = data['fin_trx_id']


class APaginated:
    """
    Represents a paginated response.

    Args:
        data (dict): The paginated data.

    Attributes:
        count (int): The total number of items.
        next (str, optional): The URL to the next page.
        previous (str, optional): The URL to the previous page.
    """

    def __init__(self, data: Dict[str, Any]):
        self.count: int = data['count']
        self.next: Optional[str] = data.get('next')
        self.previous: Optional[str] = data.get('previous')


class Wallet:
    """
    Represents a wallet.

    Args:
        data (dict): The wallet data.

    Attributes:
        id (int): The identifier of the wallet.
        number (str): The number of the wallet.
        country (str): The country of the wallet.
        status (str): The status of the wallet.
        last_activity (datetime, optional): The last activity of the wallet.
        balance (float): The balance of the wallet.
        first_name (str, optional): The first name of the wallet.
        last_name (str): The last name of the wallet.
        email (str, optional): The email of the wallet.
        phone_number (str): The phone number of the wallet.
    """

    def __init__(self, data: Dict[str, Any]):
        self.id: int = data['identifier']
        self.number: str = data['number']
        self.country: str = data['country']
        self.status: str = data['status']
        self.last_activity: Optional[datetime] = datetime.strptime(data['last_activity'], '%Y-%m-%dT%H:%M:%SZ') \
            if data.get('last_activity') else None
        self.balance: float = data['balance']
        self.first_name: Optional[str] = data['first_name']
        self.last_name: str = data['last_name']
        self.email: Optional[str] = data['email']
        self.phone_number: str = data['phone_number']
        self.gender = data['gender']

    def __str__(self):
        return self.number


class PaginatedWallets(APaginated):
    """
    Represents a paginated response of wallets.

    Args:
        data (dict): The paginated data.

    Attributes:
        results (List[Wallet]): The list of wallets.
    """

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.results: List[Wallet] = [Wallet(w) for w in data['results']]


class PaginatedWalletTransactions(APaginated):
    """
    Represents a paginated response of wallet transactions.

    Args:
        data (dict): The paginated data.

    Attributes:
        results (List[WalletTransaction]): The list of transactions.
    """

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.results: List[WalletTransaction] = [WalletTransaction(t) for t in data['results']]


class Contribution(ATransaction):
    """
    Represents a transaction.
    This class extends :ATransaction:. It adds more attributes to the transaction.

    Args:
        data (dict): The transaction data.

    Attributes:
        pk (str): The primary key of the transaction.
        status (str): The status of the transaction.
        type (str): The type of the transaction.
        amount (float): The amount of the transaction.
        fees (float, optional): The fees of the transaction.
        b_party (str): The b party of the transaction.
        message (str, optional): The message of the transaction.
        service (str): The service of the transaction.
        reference (str, optional): The reference of the transaction.
        date (datetime): The timestamp of the transaction.
        country (str): The country of the transaction.
        currency (str): The currency of the transaction.
        fin_trx_id (str, optional): The financial transaction ID of the transaction.
        trxamount (float, optional): The transaction amount.
        location (Location, optional): The location of the transaction.
        contributor (Customer, optional): The contributor of the transaction.
    """

    def __init__(self, data: dict):
        super().__init__(data)
        self.contributor: Optional[Customer] = Customer(data['contributor']) if data.get('contributor') else None

    def __str__(self):
        return self.pk


class ContributionResponse:
    """
    Represents the response of a transactional operation.

    Args:
        data (dict): The response data from the server.

    Attributes:
        success (bool): Whether the operation was successful.
        message (str, optional): The message returned by the operation.
        contribution (Contribution): The transaction object.
        status (str): The status of the transaction.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

        self.success: bool = data['success']
        self.message: Optional[str] = data['message']
        self.contribution: Contribution = Contribution(data['contribution'])
        self.status: str = data['status']

    def __str__(self):
        return '{}: {}'.format(self.status, self.message)

    def is_operation_success(self):
        """ """
        return self.success

    def is_contribution_success(self):
        """ """
        return self.contribution.is_success()

    def get_data(self) -> Dict[str, Any]:
        return self._data
