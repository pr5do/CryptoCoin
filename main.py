import rsa
import time
from hashlib import sha256

data = []

def generate_public_and_private_key():
	(private_key, public_key) = rsa.newkeys(512)
	return {'private_key': private_key, 
	'public_key' : public_key
	}

class Block():
	def __init__(self, data, index, prev_hash):
		self.data = data
		self.index = index
		self.prev_hash = prev_hash
	def mining(self):
		nonce = 0
		print("-" * 10, "Mining Block...", "-" * 10)
		while True:
			block_string = "{}{}{}{}{}".format(self.index, self.prev_hash, self.data, self.timestamp, str(nonce))
			block_string_hashed = sha256(block_string.encode('ascii')).hexdigest()
			if block_string_hashed.startswith("0" * 15):
				print("-" * 10, "Block Mined!", "-" * 10)
				proof_of_work = block_string_hashed
				self.nonce = nonce
				self.hash = block_string_hashed
				self.timestamp = time.time()
				return proof_of_work

class Transaction():
	def __init__(self, sender_public_key, recipient_public_key, sender_private_key, value):
		self.sender_public_key = sender_public_key
		self.recipient_public_key = recipient_public_key
		self.sender_private_key = sender_public_key
		self.value = value

	def sign_transaction(self):
		public_transaction = {'sender_public_key': self.sender_public_key, 
		'recipient_public_key' : self.recipient_public_key,   
		'value' : self.value
		}
		signature = rsa.sign(str(public_transaction).encode(), self.sender_private_key, 'SHA-256')
		public_transaction['signature'] = signature
		data.append(public_transaction)
		return public_transaction


if __name__ == '__main__':
	sender_pair_of_keys = generate_public_and_private_key()
	recipient_pair_of_keys = generate_public_and_private_key()

	sender_public_key = sender_pair_of_keys['public_key']
	sender_private_key = sender_pair_of_keys['private_key']

	recipient_public_key = recipient_pair_of_keys['public_key'
	zero = Transaction(sender_public_key, recipient_public_key, sender_private_key, 10)
	zero.sign_transaction()
	print(dir(zero))
