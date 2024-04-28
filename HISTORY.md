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
