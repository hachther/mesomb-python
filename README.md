# PyMeSomb

Python SDK for [MeSomb](https://docs.mesomb.com) services.

- Official API schema: https://mesomb.hachther.com/en/api/v1.1/schema/
- Homepage: https://mesomb.com
- License: MIT

## Installation

```bash
pip install pymesomb
```

## Quick Start

> Important: all operation methods use **keyword arguments** (not a single dict argument).

```python
from pymesomb.operations import PaymentOperation

operation = PaymentOperation(
    application_key="YOUR_APPLICATION_KEY",
    access_key="YOUR_ACCESS_KEY",
    secret_key="YOUR_SECRET_KEY",
)

response = operation.make_collect(
    amount=100,
    service="MTN",
    payer="670000000",
)

print(response.status)
print(response.is_operation_success())
print(response.is_transaction_success())
```

## Configuration

By default, requests target the MeSomb host configured by the SDK. For local testing you can override it:

```python
from pymesomb import mesomb

```

## Payment Use Cases

### 1) Collect money (basic)

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.make_collect(
    amount=100,
    service="MTN",
    payer="670000000",
    trx_id="order-1001",
)

print(res.status, res.transaction.reference)
```

### 2) Collect money with customer, location, and `line_items`

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.make_collect(
    amount=1000,
    service="MTN",
    payer="670000000",
    trx_id="order-1002",
    customer={
        "phone": "+237677550439",
        "email": "fisher.bank@gmail.com",
        "first_name": "Fisher",
        "last_name": "BANK",
    },
    location={
        "town": "Douala",
        "region": "Littoral",
        "country": "Cameroon",
    },
    line_items=[
        {
            "product_data": {"name": "Sac a Main"},
            "unit_amount": 1000,
            "quantity": 1,
            "currency": "XAF",
        }
    ],
)

print(res.transaction.amount, res.transaction.currency)
```

### 3) Deposit money

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.make_deposit(
    amount=1500,
    service="ORANGE",
    receiver="690000000",
    trx_id="payout-9001",
)

print(res.status)
```

### 4) Airtime purchase

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.purchase_airtime(
    amount=500,
    service="MTN",
    receiver="670000000",
    merchant="MTN",
    trx_id="airtime-001",
)

print(res.status)
```

### 5) Yango refill

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.make_yango_refill(
    amount=2000,
    service="MTN",
    payer="670000000",
    driver_id="DRIVER_123",
    trx_id="yango-001",
)

print(res.status)
```

### 6) Refund

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

res = payment.refund_transaction(
    trx_id="MESOMB_TRANSACTION_ID",
    amount=100,
    currency="XAF",
)

print(res.status)
```

### 7) Get payment app status and transactions

```python
from pymesomb.operations import PaymentOperation

payment = PaymentOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

status = payment.get_status()
print(status.name, status.countries)

transactions = payment.get_transactions(["ID1", "ID2"], source="MESOMB")
print(len(transactions))
```

## Checkout Use Cases

### Create checkout session

```python
from pymesomb.operations import CheckOutOperation

checkout = CheckOutOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

session = checkout.create(
    amount="1200",  # decimal string supported by API schema
    success_url="https://merchant.local/success",
    cancel_url="https://merchant.local/cancel",
    client_reference_id="ORD-1001",
    line_items=[
        {
            "product": "prod_001",
            "unit_amount": 1200,
            "quantity": 1,
            "currency": "XAF",
        }
    ],
    fees_included=True,
    secure_pay={
        "terms_accepted": True,
        "pay_mode": "optional",
        "dispute_enabled": True,
    },
)

print(session.id)
print(session.url)
```

### Retrieve, expire, and delete checkout session

```python
from pymesomb.operations import CheckOutOperation

checkout = CheckOutOperation("APP_KEY", "ACCESS_KEY", "SECRET_KEY")

session = checkout.retreive("cs_xxx")  # SDK method name is `retreive`
print(session.status)

expired = checkout.expire("cs_xxx")
print(expired.status)

deleted = checkout.delete("cs_xxx")
print(deleted)
```

## Wallet Use Cases

```python
from pymesomb.operations import WalletOperation

wallet = WalletOperation("PROVIDER_KEY", "ACCESS_KEY", "SECRET_KEY")

created = wallet.create_wallet(
    last_name="DOE",
    first_name="John",
    phone_number="670000000",
    gender="M",
)

print(created.id, created.number)
```

## Fundraising Use Cases

```python
from pymesomb.operations import FundraisingOperation

fund = FundraisingOperation("FUND_KEY", "ACCESS_KEY", "SECRET_KEY")

res = fund.make_contribution(
    amount=1000,
    service="MTN",
    payer="670000000",
    full_name={"last_name": "DOE", "first_name": "John"},
    contact={"phone_number": "670000000"},
    accept_terms=True,
)

print(res.status)
```

## Error Handling

```python
from pymesomb.exceptions import (
    ServiceNotFoundException,
    PermissionDeniedException,
    InvalidClientRequestException,
)

try:
    # your operation call here
    pass
except ServiceNotFoundException as exc:
    print("Service not found:", exc)
except PermissionDeniedException as exc:
    print("Permission denied:", exc)
except InvalidClientRequestException as exc:
    print("Invalid request:", exc)
```

## Changelog

### 2.1.3 (2026-11-21)

- Rename base url
- Fix parsing error

### 2.1.1 (2026-05-06)

- Rename products to line_items to improve clarity.
- Add secure payment in checkout creation.

### 2.1.0 (2026-04-23)

- Integration of checkout operation to create a checkout session and get the checkout URL.
- Integration of customer and product management operations.

### 2.0.3 (2025-03-24)

- Add purchase_airtime to depose airtime in an account.

### 2.0.2 (2025-03-12)

- Rename identifier to id in WalletTransaction.

### 2.0.1 (2025-03-12)

- Add get_transactions method to retrieve transactions based on IDs and external IDs.
- Rename get_transactions to list_transactions in wallet operation.
- Improve canonical query handling in signature.py.

### 2.0.0 (2025-02-10)

- Add fundraising operations.
- Add wallet operations.
- Add refund transaction operation.

#### Breaking changes

- Parameters for make_collect and make_deposit are no longer passed as a dict, but as keyword arguments.
- Remove security operations.
- Change parameter ts(str) to date(datetime) in Transaction class.

### 1.1.1 (2025-01-31)

- Integration of Yango refill.

### 1.1.0 (2024-09-02)

- Add wallet operations: create wallet, update wallet, get wallet, delete wallet, adjust wallet and list wallets.

### 1.0.4 (2024-04-28)

- Add function to detect phone number operator in Cameroon.

### 1.0.3 (2024-01-24)

- Handle case when trxID is not string.
- Fix crash to display response.
- Add raw_response in TransactionResponse to store MeSomb response.

### 1.0.2 (2023-07-25)

#### Breaking changes

- Only one parameter is now passed to make_deposit and make_collect. The parameter is a map that contains all details of your request.
- All methods now return MeSomb models, not dict.

### 1.0.0 (2022-10-20)

- First release of the module.

For canonical release history, you can also check `HISTORY.md`.

## Author

Hachther LLC `<contact@hachther.com>`

- Website: https://www.hachther.com
- Twitter: https://twitter.com/hachther
- GitHub: https://github.com/hachther
- LinkedIn: https://linkedin.com/in/hachther
