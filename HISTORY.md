# 2.0.0 (2025-02-10)
## Added
- Add fundraising operations
- Add wallet operations
- Add refund transaction operation
## === BREAKING CHANGES ===
- Parameters for make_collect and make_deposit are not more passed as dict but as keyword arguments
- Remove security operations
- Change parameter ts(str) to date(datetime) in Transaction class

# 1.1.1 (2025-01-31)
- Integration of Yango refill

# 1.1.0 (2024-09-02)
- Add wallet operations: create wallet, update wallet, get wallet, delete wallet, adjust wallet and list wallets.

# 1.0.4 (2024-04-28)
- Add function to detect phone number operator in cameroon

# 1.0.3 (2024-01-24)
- Handle case when trxID is not string 
- Fix crash to display response
- Add raw_response in TransactionResponse to store MeSomb response.

# 1.0.2 (2023-07-25)
## === BREAKING CHANGES ===
Only one parameter is now passed to make_deposit and make_collect. The parameter is a Map that will contain all details of your request.

All method is now returning MeSomb model not dict

# 1.0.0 (2022-10-20)
First release of the module.
