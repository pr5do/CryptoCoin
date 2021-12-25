import binascii
from Crypto.PublicKey import RSA
import Crypto
from Crypto.Hash import SHA256
from Crypto.Signature import *
import datetime
import time
from hashlib import sha256
import getpass


def generate_public_and_private_key():
	private_key = RSA.generate(1024)
	public_key = private_key.publickey()
	return {'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
	'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}
class Blockchain():
	def __init__(self):
		self.chain = []
		self.current_data = []
		self.construct_genesis()
	def construct_genesis(self):
		self.construct_block()
	def construct_block(self, prev_hash='0' * 64):
		block = Block(data = self.current_data, 
		index = len(self.chain), 
		prev_hash = prev_hash)
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
		def generator():
			while True:
				yield
		nonce = 0
		while True:
			block_string = "{}{}{}{}".format(self.index, self.prev_hash, self.data, str(nonce))
			block_string_hashed = sha256(block_string.encode('ascii')).hexdigest()
			if block_string_hashed.startswith("0" * 5):
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
		public_transaction = {'sender_public_key': self.sender_public_key, 
		'recipient_public_key' : self.recipient_public_key,   
		'value' : self.value
		}
		
		private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
		signer = PKCS1_v1_5.new(private_key)
		h = SHA256.new(str(public_transaction).encode('utf8'))
		signature = binascii.hexlify(signer.sign(h)).decode('ascii')
		public_transaction['signature'] = signature
		return public_transaction

def main():
	blockchain = Blockchain()
	print('-' * 30 + ' Welcome to the Cryptocoin! ' + "-" * 30)
	while True:
		time.sleep(1)
		print('Choose between the options below')
		time.sleep(1)
		print()
		print('[1]: Add a new transaction')
		time.sleep(1)
		print('[2]: Mine a block')
		time.sleep(1)
		print('[3]: Quit')
		time.sleep(1)
		while True:
			print()
			choice = int(getpass.getpass('Type: '))
			if choice <=3 and choice > 0:
				break
			else:
				print()
				print("Invalid value! Answer only 1, 2 or 3!")
		if choice == 1:
			print()
			print("You choosed to add a new transaction.")
			print()
			time.sleep(1)
			print("Do you have a pair of keys? Answer \"y\" or \"n\"")
			time.sleep(1)
			while True: 
				print()
				answer = getpass.getpass('Type: ').replace(" ", "").lower()[0]
				if answer == "y" or answer == "n":
					break  
				else:
					print("Invalid value! Answer only \"y\" or \"n\"!")
			while True:
				if answer == "y":
					print()
					sender_private_key = input("Type your private key: ").replace(" ", "")
					time.sleep(1)
					sender_public_key = input("Type your public key: ").replace(" ", "")
					time.sleep(1)
					recipient_public_key = input("Type the public key of the person you want to transact: ").replace(" ", "").encode()
					time.sleep(1)
					value = int(input("Type the value of the transaction: "))
					transaction = Transaction(sender_public_key, recipient_public_key, sender_private_key, value)
					public_transaction = transaction.sign_transaction()
					blockchain.add_transaction(public_transaction)
					time.sleep(1)
					print('Trasaction successfully registered!')
					print("-" * 30)
					break
				if answer == "n":
					print()
					pair_of_keys = generate_public_and_private_key()
					time.sleep(1)
					print(f"Your public key: {pair_of_keys['public_key']}")
					time.sleep(1)
					print()
					print(f"Your private key: {pair_of_keys['private_key']}")
					time.sleep(1)
					answer = "y"
		if choice == 2:
			print()
			print("You choosed to mine a block.")
			print()
			print('Mining block...')
			attr = vars(blockchain.chain[-1])
			prev_hash = attr['hash']
			print()
			blockchain.construct_block(prev_hash)
			print("Block mined and added to the blockchain successfully!")
			print()
			time.sleep(1)
			print("-" * 30)

		if choice == 3:
			break

if __name__ == '__main__':
	#recipient_pair_of_keys = generate_public_and_private_key()

	#recipient_public_key = recipient_pair_of_keys['public_key']

	#print(f'Recipient public key: {recipient_public_key}')
	
	main()
	