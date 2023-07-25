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
