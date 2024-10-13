import pytest
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account
from algosdk.v2client import algod
from pyteal import *

algod_address = "https://testnet-api.4160.nodely.dev/" # https://mainnet-api.4160.nodely.dev/
algod_token = ""
mnemonic_phrase = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"

algod_client = algod.AlgodClient(algod_token, algod_address)

def approval_program():
    return compileTeal(
        Seq([
            App.globalPut(Bytes("ebook_owner"), Txn.sender()),
            App.globalPut(Bytes("ebook_id"), Int(0)),
            Return(Int(1))
        ]),
        mode=Mode.Application
    )

def clear_state_program():
    return compileTeal(
        Return(Int(1)),
        mode=Mode.Application
    )

def deploy_contract():
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_address = account.address_from_private_key(account_private_key)

    txn = transaction.ApplicationCreateTxn(
        sender=account_address,
        sp=algod_client.suggested_params(),
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program(),
        clear_program=clear_state_program()
    )

    signed_txn = txn.sign(account_private_key)
    txid = algod_client.send_transaction(signed_txn)
    return txid

def test_deploy_contract():
    txid = deploy_contract()
    assert txid is not None

def test_approval_program():
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_address = account.address_from_private_key(account_private_key)

    txn = transaction.ApplicationCallTxn(
        sender=account_address,
        sp=algod_client.suggested_params(),
        index=1,  # replace with actual app ID
        on_complete=transaction.OnComplete.NoOpOC
    )

    signed_txn = txn.sign(account_private_key)
    txid = algod_client.send_transaction(signed_txn)
    assert txid is not None

def test_clear_state_program():
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_address = account.address_from_private_key(account_private_key)

    txn = transaction.ApplicationCallTxn(
        sender=account_address,
        sp=algod_client.suggested_params(),
        index=1,  # replace with actual app ID
        on_complete=transaction.OnComplete.DeleteOC
    )

    signed_txn = txn.sign(account_private_key)
    txid = algod_client.send_transaction(signed_txn)
    assert txid is not None