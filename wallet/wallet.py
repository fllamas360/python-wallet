# Import dependencies
import subprocess
import json
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
 
 
 
# Create a function called `derive_wallets`
def derive_wallets(coin, mnemonic, numderive):
    command = f".derive -g --coin="{coin}" --mnemonic="{mnemonic}" --numderive={numderive} --format=json --cols=path, address, priv_key"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(ETH, mnemonic, numderive),
    BTCTEST: derive_wallets(BTCTEST, mnemonic, numderive)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
   
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx( ):
   

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx( ):
     

