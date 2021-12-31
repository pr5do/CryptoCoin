import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random
import datetime
from hashlib import sha256
import secrets
import string


def generate_public_and_private_key():
	keysize = 2048

	random_generator = Random.new().read
	key = RSA.generate(keysize, random_generator)
	private_key, public_key = key, key.publickey()

	return (private_key, public_key)

def verify_signature(public_transaction_without_signature, signature, public_key):
	pass



def random_string_generator():
	characters = string.ascii_letters + string.digits

	secure_password = ''.join(secrets.choice(characters) for i in range(100))	

	return secure_password


class Blockchain():
	def __init__(self):
		self.chain = []
		self.current_data = []
		self.construct_genesis()

	def construct_genesis(self):
		genesis = self.construct_block()

		return True, genesis	

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

	def sign_transaction(self):

		public_transaction = {'sender_public_key': 
			binascii.hexlify(self.sender_public_key.exportKey('PEM', random_string_generator())),
			'recipient_public_key': 
			binascii.hexlify(self.recipient_public_key.exportKey('PEM', random_string_generator())),
			'value': self.value
		}
		
		private_key = self.sender_private_key
		signer = PKCS1_v1_5.new(private_key)

		hash_object = SHA256.new(str(public_transaction).encode('utf8'))
		hash_object.update(random_string_generator().encode('utf8'))

		signature = binascii.hexlify(signer.sign(hash_object))

		public_transaction['signature'] = str(signature)

		return public_transaction
