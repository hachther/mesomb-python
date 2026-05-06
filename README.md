<h1 align="center">Welcome to pymesomb 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://mesomb.hachther.com/en/api/v1.1/schema/" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/hachther" target="_blank">
    <img alt="Twitter: hachther" src="https://img.shields.io/twitter/follow/hachther.svg?style=social" />
  </a>
</p>

> Python client for MeSomb Services
> 
> You can check the full [documentation of the api here](https://mesomb.hachther.com/en/api/v1.1/schema/)

### 🏠 [Homepage](https://mesomb.com)

## Install

```sh
pip3 install pymesomb
```

## Usage

### Collect money from an account

```python
from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime

operation = PaymentOperation('<application_key>', '<access_key>', '<secret_key>')
response = operation.make_collect({
    'amount': 100,
    'service': 'MTN',
    'payer': '670000000',
    'date': datetime.now(),
    'nonce': RandomGenerator.nonce(),
    'trxID': '1'
})
print(response.is_operation_success())
print(response.is_transaction_success())
```

### Depose money in an account

```python
from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime

operation = PaymentOperation('<application_key>', '<access_key>', '<secret_key>')
response = operation.make_deposit({
    'amount': 100,
    'service': 'MTN',
    'receiver': '670000000',
    'date': datetime.now(),
    'nonce': RandomGenerator.nonce(),
    'trxID': '1'
})
print(response.is_operation_success())
print(response.is_transaction_success())
```

### Get application status

```python
from pymesomb.operations import PaymentOperation

operation = PaymentOperation('<application_key>', '<access_key>', '<secret_key>')
response = operation.get_status()
print(response.name)
```

### Get transactions by IDs

```python
from pymesomb.operations import PaymentOperation

operation = PaymentOperation('<application_key>', '<access_key>', '<secret_key>')
response = operation.get_transactions(['ID1', 'ID2'])
print(response)
```

## Author

👤 **Hachther LLC <contact@hachther.com>**

* Website: https://www.hachther.com
* Twitter: [@hachther](https://twitter.com/hachther)
* Github: [@hachther](https://github.com/hachther)
* LinkedIn: [@hachther](https://linkedin.com/in/hachther)

## Show your support

Give a ⭐️ if this project helped you!

## Changes log

### 2.1.0 (2026-04-23)
- Integration of checkout operation to create a checkout session and get the checkout url
- Integration of customer and product management operations

### 2.0.3 (2025-03-24)
- Add purchase_airtime to depose airtime in an account

### 2.0.2 (2025-03-12)
- Rename identifier to id in WalletTransaction

### 2.0.1 (2025-03-12)

- [Added] Add get_transactions method to retrieve transactions based on ids and external ids
- [Update] Rename get_transactions to list_transactions in wallet operation
- [Update] Improve canonical query handling in signature.py

### 2.0.0 (2025-02-10)

- [Added] Add fundraising operations
- [Added] Add wallet operations
- [Added] Add refund transaction operation

#### === BREAKING CHANGES ===
- Parameters for make_collect and make_deposit are not more passed as dict but as keyword arguments
- Remove security operations
- Change parameter ts(str) to date(datetime) in Transaction class

### 1.1.1 (2025-01-31)
- Integration of Yango refill

### 1.1.0 (2024-09-02)
- Add wallet operations: create wallet, update wallet, get wallet, delete wallet, adjust wallet and list wallets.

### 1.0.4 (2024-04-28)
- Add function to detect phone number operator in cameroon

### 1.0.3 (2024-01-24)
- Handle case when trxID is not string 
- Fix crash to display response
- Add raw_response in TransactionResponse to store MeSomb response.

### 1.0.2 (2023-07-25)
#### === BREAKING CHANGES ===
Only one parameter is now passed to make_deposit and make_collect. The parameter is a Map that will contain all details of your request.

All method is now returning MeSomb model not dict

### 1.0.0 (2022-10-20)
First release of the module.
