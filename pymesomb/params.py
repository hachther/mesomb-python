from typing import Dict, List

try:
    from typing import TypedDict, Required, NotRequired
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict, Required, NotRequired


class AddressPayload(TypedDict, total=False):
    """Postal address payload (Address schema).

    Attributes:
        line1: First line of the street address.
        region: Region/state/province of the address.
        town: Town/city of the address.
        country: Two-letter country code.
        line2: Optional second line of the street address.
        zip: Optional postal or ZIP code.
    """

    line1: Required[str]
    region: Required[str]
    town: Required[str]
    country: str
    line2: str
    zip: str


class CustomerPayload(TypedDict, total=False):
    """Customer payload used by payment/checkout/customer operations.

    Attributes:
        email: Customer contact email.
        phone: Customer contact phone number.
        town: Customer town/city.
        region: Customer region/state.
        country: Customer country code/name.
        first_name: Customer first name.
        last_name: Customer last name.
        address: Optional structured address payload.
    """

    email: str
    phone: str
    town: str
    region: str
    country: str
    first_name: str
    last_name: str
    address: AddressPayload


class LocationPayload(TypedDict, total=False):
    """Location payload (Location schema).

    Attributes:
        town: Town where the transaction happened.
        region: Optional region where the transaction happened.
        country: Optional country where the transaction happened.
        ip: Optional IP address used for geolocation.
    """

    town: str
    region: str
    country: str
    ip: str


class OnlinePaymentProductPayload(TypedDict, total=False):
    """Product line payload used by payment operations.

    Attributes:
        id: Product identifier in your catalog.
        quantity: Quantity of this product line.
        amount: Subtotal amount for this product line.
    """

    id: Required[str]
    quantity: int
    amount: float


class ContactPayload(TypedDict, total=False):
    """Fundraising contact payload (Contact schema).

    Attributes:
        phone_number: Contributor phone number.
        email: Optional contributor email.
    """

    phone_number: Required[str]
    email: str


class FullNamePayload(TypedDict, total=False):
    """Fundraising full name payload (FullName schema).

    Attributes:
        last_name: Contributor last name.
        first_name: Optional contributor first name.
    """

    last_name: Required[str]
    first_name: str


class CheckoutSessionLineItemProductDataPayload(TypedDict, total=False):
    """Inline ``product_data`` object for checkout line items.

    Attributes:
        name: Product name displayed in checkout.
        description: Optional product description.
        metadata: Optional metadata associated with this product.
        images: Optional list of product image URLs.
        unit_label: Optional text label for product unit.
    """

    name: Required[str]
    description: str
    metadata: Dict[str, object]
    images: List[str]
    unit_label: str


class CheckoutSessionLineItemPayload(TypedDict, total=False):
    """CheckoutSessionLineItem payload used in CreateCheckoutSession.

    Attributes:
        product: Existing product identifier.
        unit_amount: Unit amount to charge.
        currency: Currency for this line item.
        quantity: Quantity for this line item.
        product_data: Optional inline product data when creating ad-hoc product details.
    """

    product: Required[str]
    unit_amount: Required[float]
    currency: str
    quantity: int
    product_data: CheckoutSessionLineItemProductDataPayload


class BrandingSettingsPayload(TypedDict, total=False):
    """Checkout branding settings payload.

    Attributes:
        background_color: Checkout widget background color (hex value).
        border_style: Border style for widget rendering.
        button_color: Checkout pay button color (hex value).
        display_name: Custom business name shown on checkout.
        font_family: Font family used by checkout UI.
    """

    background_color: str
    border_style: str
    button_color: str
    display_name: str
    font_family: str


class CheckoutConsentCollectionPayload(TypedDict, total=False):
    """Checkout consent collection configuration payload.

    Attributes:
        promotions: Promotion consent collection mode.
        terms_of_service: Terms of service acceptance mode.
    """

    promotions: str
    terms_of_service: str


class PaymentCustomFieldPayload(TypedDict, total=False):
    """Payment custom field payload.

    Attributes:
        type: Field input type (for example ``text`` or ``number``).
        label: Field label displayed to the customer.
        set_limit: Enable value range limitation for this field.
        optional: Allow this field to be left empty.
        limit_type: Limit comparison mode (min/max/between/equal).
        limit_min: Minimum accepted value.
        limit_max: Maximum accepted value.
    """

    type: Required[str]
    label: Required[str]
    set_limit: bool
    optional: bool
    limit_type: str
    limit_min: float
    limit_max: float


class CheckoutCustomTextPayload(TypedDict, total=False):
    """Checkout custom text payload.

    Attributes:
        after_submit: Text displayed after submit button.
        submit: Text displayed near submit button.
        terms_of_service_acceptance: Text used for terms acceptance label.
    """

    after_submit: str
    submit: str
    terms_of_service_acceptance: str


class CheckoutDiscountPayload(TypedDict, total=False):
    """Checkout discount payload.

    Attributes:
        coupon: Coupon identifier to apply.
        promotion_code: Promotion code identifier to apply.
    """

    coupon: str
    promotion_code: str


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
    address: AddressPayload
    metadata: Dict[str, object]
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
        line_items: Optional checkout line items.
        branding_settings: Optional branding settings payload.
        consent_collection: Optional consent collection configuration.
        custom_fields: Optional list of checkout custom fields.
        custom_text: Optional custom text blocks.
        discounts: Optional discount/coupon payload.
        required_contact_info: Ask customer contact information when true.
        call_to_action: Checkout submit button type.
        metadata: Optional custom key-value metadata.
        conversion: Enable amount conversion when needed.
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
    customer: CustomerPayload
    location: LocationPayload
    line_items: List[CheckoutSessionLineItemPayload]
    branding_settings: BrandingSettingsPayload
    consent_collection: CheckoutConsentCollectionPayload
    custom_fields: List[PaymentCustomFieldPayload]
    custom_text: CheckoutCustomTextPayload
    discounts: CheckoutDiscountPayload
    required_contact_info: bool
    call_to_action: str
    metadata: Dict[str, object]
    conversion: NotRequired[bool]
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
    location: NotRequired[LocationPayload]
    products: NotRequired[List[OnlinePaymentProductPayload]]
    customer: NotRequired[CustomerPayload]
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
    location: NotRequired[LocationPayload]
    products: NotRequired[List[OnlinePaymentProductPayload]]
    customer: NotRequired[CustomerPayload]
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
    location: NotRequired[LocationPayload]
    products: NotRequired[List[OnlinePaymentProductPayload]]
    customer: NotRequired[CustomerPayload]
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
    location: NotRequired[LocationPayload]
    customer: NotRequired[CustomerPayload]
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
    location: NotRequired[LocationPayload]
    contact: ContactPayload
    full_name: FullNamePayload
    trx_id: str


