
from login import login

# Process needed to run the files on the /model folder
import sys
sys.path.insert(0, "C:/Users/gusta\OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from blockchain import Blockchain, Transaction, generate_private_and_public_key
from database_manager import change_public_and_private_key_status, store_public_key,get_public_and_private_key_status

from termcolor import colored
import getpass
import time
import os


def generate_public_and_private_key_for_user(username):
	time.sleep(1)
	print("We need to generate a public and private key for you")
	print()

	time.sleep(1)
	print("Generating...")
	time.sleep(2)

	user_private_key, user_public_key = generate_private_and_public_key()

	print(f"Your public key is: {user_public_key.export_key(format='OpenSSH').split()[1]}")
	print()
	time.sleep(1)

	store_public_key(username, user_public_key.export_key(format='OpenSSH').split()[1])

	print(colored("We automatically stored it for you!", "green"))

	print()
	private_key_passphrase = getpass.getpass("Enter the passphrase for your private key: ").replace(" ", "")
	print()
	time.sleep(1)

	print(colored("Attention! if you lose your passphrase you will not be able to make transactions in your account", "yellow"))
	print(colored("Store your private key in some safe place!", 'yellow'))

	print()

	print(f"Your private key is: {user_private_key.export_key(format='PEM', passphrase=private_key_passphrase, protection='PBKDF2WithHMAC-SHA1AndAES128-CBC')}")

	change_public_and_private_key_status(username, user_public_key.export_key(format='OpenSSH').split()[1])

	return True
	

def add_transaction_to_current_data():
	print()
	print("You choosed to add a new transaction.")
	print()
	time.sleep(1)
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

	# Deleting the private key from the transaction for security purposes
	delattr(transaction, 'sender_private_key')

	Blockchain.add_transaction(public_transaction)
	time.sleep(1)
	print('Trasaction successfully registered!')
	print("-" * 30)			


def app():
	status, username = login()
	if status == True:
		os.system('cls||clear')
		blockchain = Blockchain()
		print()
		time.sleep(1)
		print('-' * 30 + f' Welcome to the Cryptocoin, {username}! ' + "-" * 30)
		while True:
			if get_public_and_private_key_status(username) == (0,):
				generate_public_and_private_key_for_user(username)
			else:
				while True:
						print()
						time.sleep(1)
						print('Choose between the options below:')
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
								if choice <= 3 and choice > 0:
										break
								else:
										print()
										print(colored("Invalid value! Answer only 1, 2 or 3!", "red"))
						if choice == 1:
							add_transaction_to_current_data()
											
						if choice == 2:
								print()
								print("You choosed to mine a block.")
								print()
								print('Mining block...')
								attr = vars(blockchain.chain[-1])
								prev_hash = attr['hash']
								print()
								blockchain.construct_block(prev_hash)
								print("Block mined and added to the successfully!")
								print()
								time.sleep(1)
								print("-" * 30)

						if choice == 3:
							os.system('cls||clear')
							time.sleep(1)
							text = f"Goodbye, {username}!"
							print(colored(text, 'green'))
							time.sleep(1)
							os.system('cls||clear')
							return True
	else:
			print(colored("Error during login", "red"))
			return False


if __name__ == '__main__':
    app()
