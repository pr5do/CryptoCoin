from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA384
import datetime
from hashlib import sha256


def generate_private_and_public_key():
    """
    Generates EccKey object public and private ECDSA key
    """

    key = ECC.generate(curve='secp384r1')
    private_key, public_key = key, key.public_key()
    return (private_key, public_key)


def verify_transaction(public_transaction):
    """
    Verifies if a transaction is valid or not based on his signature

        Parameters:
            public_transaction (dict): public keys and value of the transaction

        Returns:
            response (tuple): boolean and string saying if the transaction is
            valid or not
    """

    public_key = public_transaction['sender_public_key']

    public_transaction_without_signature_and_hash = {
        'sender_public_key': public_transaction['sender_public_key'],
        'recipient_public_key': public_transaction['recipient_public_key'],
        'value': public_transaction['value']
    }

    hash_object = SHA384.new(
        str(public_transaction_without_signature_and_hash).encode('utf8'))

    try:
        DSS.new(public_key, 'fips-186-3').verify(hash_object,
                                                 public_transaction['signature'])
        return True, "This transaction is valid"

    except (ValueError):
        return False, "This transaction is not valid"


class Blockchain():
    """

    Class that creates a entire blockchain

    Attributes
    -----------

    chain: list
        all the blocks on the chain
    current_data: list
        all the unconfirmed transactions (transactions that aren't in a block)

    Methods:
    ----------

        construct_genesis():
            generates the genesis block (first block on the blockchain)

        construct_block(previous_hash='0' 64):
            add a block to the blockchain

        add_transaction(transaction):
            adds transaction to the current data

    """

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.construct_genesis()

    def construct_genesis(self):
        """

        Generates the genesis block (first block on the blockchain)


        """
        genesis = self.construct_block()

        return genesis

    def construct_block(self, previous_hash='0' * 64):
        """
        Add a block to the blockchain

        If the argument 'previous_hash' is passed, is possible to add a hash
        of a certain block

        Parameters
        -----------
            previous_hash: str, optional
                Previous hash of this block on the blockchain (default is '0'
                * 64)
        """
        block = Block(data=self.current_data, index=len(
            self.chain), previous_hash=previous_hash)

        self.current_data = []

        self.chain.append(block)

        return block

    def add_transaction(self, transaction):
        self.current_data.append(transaction)

        return True


class Block():
    """

    Class of block that can be mined and will be added to the blockchain

    Attributes:
    -----------

        data: str
            transaction will be added here

        index: int
            number of the block on the blockchain

        previous_hash: str
            hash of the previous block

        difficulty: int
            number of zeros that the proof of work must have to consider the
            block mined

        nonce: int
            number that was iterated several times to get the specific hash
            (proof of work) of the block

        hash: int
            proof of work of the block

        timestamp: str
            timestamp of the transaction

    """
    def __init__(self, data, index, previous_hash, difficulty=2):
        """
        Construct all the necessary attributes for the block

        If the difficulty is passed, the number of zeros that the hash will have
        to start will change based on the input

        Parameters:
        ------------
        data: str
            transactions of the block
        index: int
            number of the block on the blockchain

        previous_hash: str
            hash of the previous block

        difficulty: int, optional
            number of zeros that the proof of work must have to consider the
            block mined (default is 2)

        """
        self.data = data
        self.index = index
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.mining()

    def mining(self):
        """
        Mines the block based on the data, index and previous hash of the
        block plus a nonce that will change the hash of the block to make it
        start with a specific number of zeros

        Returns:
            proof_of_work : str
                proof of work of the block

        """
        def apply_sha256(text):
            return sha256(text.encode('ascii')).hexdigest()

        difficulty = self.difficulty
        nonce = 0

        while True:
            block_string = "{}{}{}{}".format(
                self.index, self.previous_hash, self.data, str(nonce))
            block_string_hashed = apply_sha256(block_string)

            if block_string_hashed.startswith("0" * difficulty):
                proof_of_work = block_string_hashed
                self.nonce = nonce
                self.hash = proof_of_work
                self.timestamp = str(datetime.datetime.now())

                return proof_of_work

            nonce += 1


class Transaction():
    """
    Class that creates a new transaction (public keys, hash, signature, value
    and timestamp)

    Attributes
    -----------

        sender_public_key: EccKey
            public key address corresponding to the sender of the transaction

        recipient_public_key: EccKey
            public key address corresponding to the destination of the transaction

        sender_private_key: EccKey
            private key corresponding  to the sender (this key will sign the
            transaction)

    """
    def __init__(self, sender_public_key, recipient_public_key,
                 sender_private_key, value):
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.sender_private_key = sender_private_key
        self.value = value

    def get_public_transaction_without_signature(self):
        """

        Get the public transaction (sender public key, recipient public key
        and value) without the signature (to later be signed)

        """
        public_transaction = {'sender_public_key': self.sender_public_key,
                              'recipient_public_key': self.recipient_public_key,
                              'value': self.value
                              }

        return public_transaction

    def sign_transaction(self):
        """

        Uses the private key of the sender attribute to sign the message.

        Also creates a unique timestamp and hash for the transaction

        """
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
    pass
