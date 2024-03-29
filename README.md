# Web3.py-Cryptnoxpy
Example of how to use Cryptnox card for signing transactions within web3.py

## Process/workflow
Upon launch the script builds a transaction with the provided details to send eth from the from_wallet_address to the to_wallet_address, an amount of eth_to_send.
Once built, the transaction is signed by the cryptnox card inserted in reader then broadcasts it to the blockchain. <br>Note: EASY MODE PIN is used for card administration.

## Prerequesites
- Cryptnox BG1 card initialized with EASY MODE and seeded.<br>(See Card initialization for more details)
- Card in reader connected to machine when running the script

## Setup
- Clone this repo
- Run `pipenv install` to install required dependencies

## Input details in script
- FROM_ADDRESS: Input wallet address to transfer from with command:<br>`nano +15 web3_cryptnox_sendeth.py`
<br> `<Input from address>` should be replaced with the wallet address to transfer from. <br> 
Example: `from_wallet_address = w3.toChecksumAddress('0x1a2b3c4d5e6f')`<br>
- TO_ADDRESS: Input wallet address to transfer to with command: <br> `nano +16 web3_cryptnox_sendeth.py`
<br> `<Input to address>` should be replaced with the wallet address to transfer to. <br> 
Example: `to_wallet_address = w3.toChecksumAddress('0x9z8x7y6w5v')`<br>
- AMOUNT_TO_SEND: Input amount of eth to transfer with command: <br><`nano +17 web3_cryptnox_sendeth.py`
<br> `0.00001` should be replaced with the desired amount to transfer. <br>
Example: `eth_to_send = 0.0256`<br>

## Running the script
- Run script with command: `python web3_cryptnox_sendeth.py`<br>
Note: Script uses EASY MODE PIN for card administration and does not prompt to ask the user for PIN.


## Card initialization

- Install cryptnoxpro with command `pip install cryptnoxpro`
- Run `cryptnox` to invoke the app
- Run `Init -e` to initialize the card
- Run `seed recover` to inject mnemonic in card
- Card is ready for use with this script
