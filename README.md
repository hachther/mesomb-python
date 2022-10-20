Python client to work with MeSomb Services

# Description

This will help your quickly integrate MeSomb API in your python project. 
You can check the [full API documentation here](https://mesomb.hachther.com/en/api/v1.1/schema/)

This contains the below elements:

- signature:
  - **sign_request**: to sign request
- payment:
  - **make_deposit**: to make a deposit operation
  - **make_payment**: to make a deposit operation
  - **update_security**: to make a deposit operation
  - **get_status**: to make a deposit operation
  - **get_transactions**: to make a deposit operation

# Installation

## Normal Installation

```bash
pip install pymesomb
```

## Development installation

```bash
git clone https://github.com/hachther/pymesomb.git
cd pymesomb
pip install --editable .
```

# Usage

## Collect money from an account

```python
from datetime import datetime
from pymesomb.payment import make_payment

configs = {
  'application_key': '<application-key>',
  'secret_key': '<secret-key>',
  'access_key': '<access-key>'
}
response = make_payment(configs, 100, 'MTN', '677550203', datetime.now(), nonce='<randomstring>')
print(response.text)
```

## Depose money in an account

```python
from datetime import datetime
from pymesomb.payment import make_deposit

configs = {
  'application_key': '<application-key>',
  'secret_key': '<secret-key>',
  'access_key': '<access-key>'
}
response = make_deposit(configs, 100, 'MTN', '677550203', datetime.now(), nonce='<random-string>')
print(response.text)
```

## Get Transaction by IDs

```python
from datetime import datetime
from pymesomb.payment import get_transactions

configs = {
  'application_key': '<application-key>',
  'secret_key': '<secret-key>',
  'access_key': '<access-key>'
}
response = get_transactions(configs, datetime.now(), ['<ID1>', '<ID2>', '...'])
print(response.text)
```