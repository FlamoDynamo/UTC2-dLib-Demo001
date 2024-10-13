import pytest
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account

algod_address = "https://testnet-api.4160.nodely.dev/" # https://mainnet-api.4160.nodely.dev/
algod_token = ""
mnemonic_phrase = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"

algod_client = algod.AlgodClient(algod_token, algod_address)

def test_get_account_info():
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_address = account.address_from_private_key(account_private_key)

    account_info = algod_client.account_info(account_address)
    assert account_info is not None
    assert account_info['address'] == account_address

def test_get_application_info():
    app_id = 1  # replace with actual app ID after deployment
    app_info = algod_client.application_info(app_id)
    assert app_info is not None
    assert app_info['id'] == app_id