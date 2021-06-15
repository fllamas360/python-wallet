# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv
import bit
from bit import wif_to_key
from bit import PrivateKeyTestnet, PrivateKey, Key
from bit.network import NetworkAPI

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
#from pathlib import path
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

 
# Create a function called `derive_wallets`
def derive_wallets(coin):
    command = f'php ./derive -g --coin="{coin} --mnemonic="{mnemonic}" --numderive=3 --format=json --cols=path, address, priv_key'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    "ETH": derive_wallets(ETH),
    "BTCTEST": derive_wallets(BTCTEST)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
   
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin,account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": to, "value": amount}
    )
        return {
        "from": account.address,
        "to": to,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }

    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

   
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        tx = create_tx(coin, account, to, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed.sendRawTransaction)

    elif coin == BTCTEST:
        tx = create_tx(coin, account, to, amount)
        signed_tx = account.send(tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

btc_test_privkey = coins["BTCTEST"][0]["address"]
btc_test_address = coins["BTCTEST"][0]["privkey"]

