from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA384
import datetime
from hashlib import sha256


def generate_private_and_public_key():
    key = ECC.generate(curve='secp384r1')
    private_key, public_key = key, key.public_key()

    return (private_key, public_key)


def verify_transaction(public_transaction):
    public_key = public_transaction['sender_public_key']

    public_transaction_without_signature_and_hash = {
        'sender_public_key': public_transaction['sender_public_key'],
        'recipient_public_key': public_transaction['recipient_public_key'],
        'value': public_transaction['value']
    }

    hash_object = SHA384.new(str(public_transaction_without_signature_and_hash).encode('utf8'))

    try:
        DSS.new(public_key, 'fips-186-3').verify(hash_object, public_transaction['signature'])
        return True, "This transaction is valid"

    except (ValueError):
        return False, "This transaction is not valid"


class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.construct_genesis()

    def construct_genesis(self):
        genesis = self.construct_block()

        return genesis

    def construct_block(self, prev_hash='0' * 64):
        block = Block(data=self.current_data, index=len(self.chain), prev_hash=prev_hash)

        self.current_data = []

        self.chain.append(block)

        return block

    def add_transaction(self, transaction):
        self.current_data.append(transaction)

        return True


class Block():
    def __init__(self, data, index, prev_hash):
        self.data = data
        self.index = index
        self.prev_hash = prev_hash
        self.mining()

    def mining(self):

        def apply_sha256(text):
            return sha256(text.encode('ascii')).hexdigest()

        difficulty = 2
        nonce = 0

        while True:
            block_string = "{}{}{}{}".format(self.index, self.prev_hash, self.data, str(nonce))
            block_string_hashed = apply_sha256(block_string)

            if block_string_hashed.startswith("0" * difficulty):
                proof_of_work = block_string_hashed
                self.nonce = nonce
                self.hash = proof_of_work
                self.timestamp = str(datetime.datetime.now())

                return proof_of_work

            nonce += 1


class Transaction():
    def __init__(self, sender_public_key, recipient_public_key, sender_private_key, value):
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.sender_private_key = sender_private_key
        self.value = value

    def get_public_transaction_without_signature(self):
        public_transaction = {'sender_public_key': self.sender_public_key,
                              'recipient_public_key': self.recipient_public_key,
                              'value': self.value
                              }

        return public_transaction

    def sign_transaction(self):
        public_transaction = self.get_public_transaction_without_signature()

        private_key = self.sender_private_key
        signer = DSS.new(private_key, 'fips-186-3')

        hash_object = SHA384.new(str(public_transaction).encode('utf8'))

        signature = signer.sign(hash_object)

        self.signature = signature

        public_transaction['signature'] = signature

        self.timestamp = str(datetime.datetime.now())
        public_transaction['timestamp'] = self.timestamp

        self.hash = sha256(str(public_transaction).encode('ascii')).hexdigest()

        public_transaction['hash'] = self.hash

        return public_transaction


if __name__ == '__main__':
    sender_private_key, sender_public_key = generate_private_and_public_key()
    recipient_private_key, recipient_public_key = generate_private_and_public_key()

    transaction = Transaction(sender_private_key, recipient_public_key, sender_private_key, 11)
    public_transaction = transaction.sign_transaction()

    print(f"Public Transaction: {public_transaction}")
    print("*" * 30)
    print(f"Signature: {verify_transaction(public_transaction)[1]}")

    blockchain = Blockchain()

    blockchain.add_transaction(public_transaction)


