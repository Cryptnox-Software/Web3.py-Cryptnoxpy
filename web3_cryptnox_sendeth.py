from turtle import towards
from eth_account._utils.legacy_transactions \
import encode_transaction,serializable_unsigned_transaction_from_dict
from web3.middleware import geth_poa_middleware
from eth_utils.curried import keccak
from hexbytes import HexBytes
import cryptnoxpy as cp
from web3 import Web3
import cryptos
import ecdsa

#Web3 variables
infura_url = "https://rinkeby.infura.io/v3/ac389dd3ded74e4a85cc05c8927825e8"
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
from_wallet_address = w3.toChecksumAddress('<Input from address>')
to_wallet_address = w3.toChecksumAddress('<Input to address>')
eth_to_send = 0.00001
eth_wei_to_send = w3.toWei(eth_to_send,'ether')


def transaction_hash(transaction, chain_id =4 ,vrs: bool = False):
        try:
            del transaction["maxFeePerGas"]
            del transaction["maxPriorityFeePerGas"]
        except KeyError:
            pass
        unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction)
        encoded_transaction = encode_transaction(unsigned_transaction, (chain_id, 0, 0))
        return keccak(encoded_transaction)


def push(transaction, signature, public_key,chain_id = 4):
        unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction)
        var_v, var_r, var_s = _decode_vrs(signature, chain_id,
                                                transaction_hash(transaction),
                                                cryptos.decode_pubkey(public_key))
        rlp_encoded = encode_transaction(unsigned_transaction, (var_v, var_r, var_s))
        return w3.eth.send_raw_transaction(HexBytes(rlp_encoded))


def _decode_vrs(signature_der: bytes, chain_id: int, transaction: bytes, q_pub: tuple) -> tuple:
        curve = ecdsa.curves.SECP256k1
        signature_decode = ecdsa.util.sigdecode_der
        generator = curve.generator
        var_r, var_s = signature_decode(signature_der, generator.order())
        var_q = ecdsa.keys.VerifyingKey.from_public_key_recovery_with_digest(
            signature_der, transaction, curve, sigdecode=signature_decode)[1]
        i = 35
        if var_q.to_string("uncompressed") == cryptos.encode_pubkey(q_pub, "bin"):
            i += 1
        var_v = 2 * chain_id + i
        return var_v, var_r, var_s


if __name__ == "__main__":
    print('Sending {0:f}'.format(eth_to_send))
    print(f'From: {from_wallet_address}')
    print(f'To: {to_wallet_address}')
    tx = {
        'nonce': w3.eth.getTransactionCount(from_wallet_address),
        'to': to_wallet_address,
        'value': eth_wei_to_send,
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei')
    }
    try:
        card = cp.factory.get_card(cp.Connection())
        card.verify_pin('12345')
        PATH = "m/44'/60'/0'/0/0"
        public_key = card.get_public_key(0x01,path=PATH,compressed=False)
        card.derive(path=PATH)
        digest = transaction_hash(tx)
        signature = card.sign(digest,pin='12345')
        print(f'Transaction hash: {bytes(push(tx,signature,public_key)).hex()}')
        print('Done!')
    except Exception as e:
        print(f'Error, please try again.\n\nError information:\n\n{e}')