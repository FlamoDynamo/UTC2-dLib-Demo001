from algosdk import mnemonic, transaction, account
from algosdk.v2client import algod
from pyteal import *

algod_address = "https://testnet-api.4160.nodely.dev/" # https://testnet-api.4160.nodely.dev/
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

def read_teal_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().encode()

def deploy_contract():
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_address = account.address_from_private_key(account_private_key)

    global_schema = transaction.StateSchema(num_uints=1, num_byte_slices=1)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    approval_program_teal = read_teal_file("../contract/approval.teal")
    clear_program_teal = read_teal_file("../contract/clear.teal")

    txn = transaction.ApplicationCreateTxn(
        sender=account_address,
        sp=algod_client.suggested_params(),
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program_teal,
        clear_program=clear_program_teal,
        global_schema=global_schema,
        local_schema=local_schema
    )

    signed_txn = txn.sign(account_private_key)
    txid = algod_client.send_transaction(signed_txn)
    return txid

if __name__ == "__main__":
    deploy_contract()