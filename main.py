import rsa
import json

def generate_public_and_private_key():
	(private_key, public_key) = rsa.newkeys(512)
	return {'private_key': private_key, 
	'public_key' : public_key
	}


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
		return public_transaction


if __name__ == '__main__':
	sender_pair_of_keys = generate_public_and_private_key()
	recipient_pair_of_keys = generate_public_and_private_key()

	sender_public_key = sender_pair_of_keys['public_key']
	sender_private_key = sender_pair_of_keys['private_key']

	recipient_public_key = recipient_pair_of_keys['public_key'
	zero = Transaction(sender_public_key, recipient_public_key, sender_private_key, 10)
	print(zero.sign_transaction())
