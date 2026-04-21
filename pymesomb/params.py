from typing import Any, Dict, List

try:
    from typing import TypedDict, Required, NotRequired
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict, Required, NotRequired


class CustomerParams(TypedDict, total=False):
    """Parameters for customer creation/update/patch operations.

    Attributes:
        email: Contact email of the customer.
        phone: Contact phone number of the customer.
        town: Customer living town.
        region: Customer living region.
        country: Customer living country code or name.
        first_name: Customer first name.
        last_name: Customer last name.
        address: Structured postal address payload.
        metadata: Custom key-value metadata linked to the customer.
        description: Internal description for the customer.
        nonce: Optional request nonce override.
    """
    email: str
    phone: str
    town: str
    region: str
    country: str
    first_name: str
    last_name: str
    address: Dict[str, Any]
    metadata: Dict[str, Any]
    description: str
    nonce: str


class ProductCreateParams(TypedDict, total=False):
    """Parameters for product creation.

    Attributes:
        name: Product display name.
        category: Optional product category.
        description: Optional product description.
        image: Optional product image URL.
        default_price: Optional default price value.
        price_type: Optional price type (for example OneTime/Recurring).
        nonce: Optional request nonce override.
    """
    name: Required[str]
    category: str
    description: str
    image: str
    default_price: str
    price_type: str
    nonce: str


class ProductUpdateParams(TypedDict, total=False):
    """Parameters for full product update (PUT).

    Attributes:
        name: Product display name.
        category: Optional product category.
        description: Optional product description.
        image: Optional product image URL.
        default_price: Optional default price value.
        price_type: Optional price type.
        nonce: Optional request nonce override.
    """
    name: Required[str]
    category: str
    description: str
    image: str
    default_price: str
    price_type: str
    nonce: str


class ProductPatchParams(TypedDict, total=False):
    """Parameters for partial product update (PATCH).

    Attributes:
        name: Product display name.
        category: Product category.
        description: Product description.
        image: Product image URL.
        default_price: Product default price value.
        price_type: Product price type.
        nonce: Optional request nonce override.
    """
    name: str
    category: str
    description: str
    image: str
    default_price: str
    price_type: str
    nonce: str


class CheckoutCreateParams(TypedDict, total=False):
    """Parameters for checkout session creation.

    Attributes:
        amount: Amount in minor units.
        success_url: URL used after successful payment.
        cancel_url: URL used after canceled payment.
        mode: Checkout mode (default is payment).
        currency: ISO currency code (default is XAF).
        description: Checkout description displayed to the payer.
        client_reference_id: Merchant-side reference for reconciliation.
        expires_in: Session expiration delay in seconds.
        customer_id: Existing customer identifier to associate.
        customer: Inline customer payload used to prefill checkout.
        location: Optional location payload for analytics.
        products: Optional checkout line items.
        metadata: Optional custom key-value metadata.
        nonce: Optional request nonce override.
    """
    amount: Required[float]
    success_url: Required[str]
    cancel_url: Required[str]
    mode: NotRequired[str]
    currency: NotRequired[str]
    description: str
    client_reference_id: str
    expires_in: int
    customer_id: str
    customer: Dict[str, Any]
    location: Dict[str, str]
    products: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    nonce: str


class CollectParams(TypedDict, total=False):
    """Parameters for payment collection.

    Attributes:
        amount: Amount to collect.
        service: Payment provider/service code.
        payer: Payer account number.
        nonce: Optional request nonce override.
        country: Country code of the transaction.
        currency: Transaction currency code.
        fees: Include MeSomb fees in charged amount when true.
        mode: Operation mode (synchronous/asynchronous).
        conversion: Enable amount conversion when needed.
        location: Customer location payload.
        products: Product items purchased in the transaction.
        customer: Customer information payload.
        trx_id: External transaction identifier.
    """
    amount: Required[float]
    service: Required[str]
    payer: Required[str]
    nonce: str
    country: NotRequired[str]
    currency: NotRequired[str]
    fees: NotRequired[bool]
    mode: NotRequired[str]
    conversion: NotRequired[bool]
    location: Dict[str, str]
    products: List[Dict[str, str]]
    customer: Dict[str, str]
    trx_id: str


class DepositParams(TypedDict, total=False):
    """Parameters for payment deposit.

    Attributes:
        amount: Amount to deposit.
        service: Payment provider/service code.
        receiver: Receiver account number.
        nonce: Optional request nonce override.
        country: Country code of the transaction.
        currency: Transaction currency code.
        conversion: Enable amount conversion when needed.
        location: Customer location payload.
        products: Product items purchased in the transaction.
        customer: Customer information payload.
        trx_id: External transaction identifier.
    """
    amount: Required[float]
    service: Required[str]
    receiver: Required[str]
    nonce: str
    country: NotRequired[str]
    currency: NotRequired[str]
    conversion: NotRequired[bool]
    location: Dict[str, str]
    products: List[Dict[str, str]]
    customer: Dict[str, str]
    trx_id: str


class AirtimeParams(TypedDict, total=False):
    """Parameters for airtime purchase.

    Attributes:
        amount: Amount to purchase.
        service: Payment provider/service code.
        receiver: Receiver account number.
        merchant: Airtime merchant/operator code.
        nonce: Optional request nonce override.
        country: Country code of the transaction.
        currency: Transaction currency code.
        location: Customer location payload.
        products: Product items purchased in the transaction.
        customer: Customer information payload.
        trx_id: External transaction identifier.
    """
    amount: Required[float]
    service: Required[str]
    receiver: Required[str]
    merchant: Required[str]
    nonce: str
    country: NotRequired[str]
    currency: NotRequired[str]
    location: Dict[str, str]
    products: List[Dict[str, str]]
    customer: Dict[str, str]
    trx_id: str


class YangoRefillParams(TypedDict, total=False):
    """Parameters for Yango refill.

    Attributes:
        amount: Amount to collect for refill.
        service: Payment provider/service code.
        payer: Payer account number.
        driver_id: Yango driver identifier.
        nonce: Optional request nonce override.
        country: Country code of the transaction.
        currency: Transaction currency code.
        mode: Operation mode (synchronous/asynchronous).
        location: Customer location payload.
        customer: Customer information payload.
        trx_id: External transaction identifier.
    """
    amount: Required[float]
    service: Required[str]
    payer: Required[str]
    driver_id: Required[str]
    nonce: str
    country: NotRequired[str]
    currency: NotRequired[str]
    mode: NotRequired[str]
    location: Dict[str, str]
    customer: Dict[str, str]
    trx_id: str


class RefundParams(TypedDict, total=False):
    """Parameters for transaction refund.

    Attributes:
        trx_id: MeSomb transaction identifier to refund.
        amount: Optional partial refund amount.
        conversion: Enable amount conversion when needed.
        currency: Currency used for the refund amount.
    """
    trx_id: Required[str]
    amount: float
    conversion: bool
    currency: str


class ContactInfoParams(TypedDict, total=False):
    """Parameters for contact information verification.

    Attributes:
        service_key: Account/phone key to verify.
        provider: Optional provider code to force lookup.
        country: Country code used for lookup.
        nonce: Optional request nonce override.
    """
    service_key: Required[str]
    provider: str
    country: NotRequired[str]
    nonce: str


class WalletCreateParams(TypedDict, total=False):
    """Parameters for wallet creation.

    Attributes:
        last_name: Wallet owner last name.
        phone_number: Wallet owner phone number.
        gender: Wallet owner gender.
        first_name: Wallet owner first name.
        country: Wallet country code.
        email: Wallet owner email.
        nonce: Optional request nonce override.
        number: Optional custom wallet number.
    """
    last_name: Required[str]
    phone_number: Required[str]
    gender: Required[str]
    first_name: str
    country: NotRequired[str]
    email: str
    nonce: str
    number: str


class WalletUpdateParams(TypedDict, total=False):
    """Parameters for wallet update.

    Attributes:
        last_name: Wallet owner last name.
        phone_number: Wallet owner phone number.
        gender: Wallet owner gender.
        first_name: Wallet owner first name.
        country: Wallet country code.
        email: Wallet owner email.
        nonce: Optional request nonce override.
    """
    last_name: Required[str]
    phone_number: Required[str]
    gender: Required[str]
    first_name: str
    country: NotRequired[str]
    email: str
    nonce: str


class WalletAddMoneyParams(TypedDict, total=False):
    """Parameters for wallet credit operation.

    Attributes:
        amount: Amount to credit.
        message: Optional transaction message.
        external_id: Optional external transaction identifier.
    """
    amount: Required[float]
    message: str
    external_id: str


class WalletRemoveMoneyParams(TypedDict, total=False):
    """Parameters for wallet debit operation.

    Attributes:
        amount: Amount to debit.
        force: Force debit even if balance is insufficient.
        message: Optional transaction message.
        external_id: Optional external transaction identifier.
    """
    amount: Required[float]
    force: NotRequired[bool]
    message: str
    external_id: str


class WalletTransferMoneyParams(TypedDict, total=False):
    """Parameters for wallet-to-wallet transfer.

    Attributes:
        amount: Amount to transfer.
        force: Force transfer even if source balance is insufficient.
        message: Optional transaction message.
        external_id: Optional external transaction identifier.
    """
    amount: Required[float]
    force: NotRequired[bool]
    message: str
    external_id: str


class FundraisingContributionParams(TypedDict, total=False):
    """Parameters for fundraising contribution.

    Attributes:
        amount: Contribution amount.
        service: Payment provider/service code.
        payer: Payer account number.
        nonce: Optional request nonce override.
        country: Country code of the transaction.
        currency: Transaction currency code.
        mode: Operation mode (synchronous/asynchronous).
        conversion: Enable amount conversion when needed.
        anonymous: Contribute anonymously when true.
        accept_terms: Confirm terms acceptance.
        location: Contributor location payload.
        contact: Contributor contact payload.
        full_name: Contributor full-name payload.
        trx_id: External transaction identifier.
    """
    amount: Required[float]
    service: Required[str]
    payer: Required[str]
    nonce: str
    country: NotRequired[str]
    currency: NotRequired[str]
    mode: NotRequired[str]
    conversion: NotRequired[bool]
    anonymous: NotRequired[bool]
    accept_terms: NotRequired[bool]
    location: Dict[str, str]
    contact: Dict[str, str]
    full_name: Dict[str, str]
    trx_id: str


