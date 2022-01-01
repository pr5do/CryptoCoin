import getpass
import time

# Process needed to run the files on the /model folder
import sys
sys.path.insert(1, "C:/Users/gusta\OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from blockchain import Blockchain, Transaction, generate_public_and_private_key
from database_manager import store_user, find_user
from termcolor import colored


def login():
	time.sleep(1)
	while True:
		print()
		print('Choose between the options below: ')
		time.sleep(1)
		print()
		print('[1]: I don\'t have an account')
		time.sleep(1)
		print()
		print('[2]: I already have an account')
		time.sleep(1)
		while True:
			print()
			choice = int(getpass.getpass('Type: '))
			if choice <= 2 and choice > 0:
				break
			else:
				print()
				print('Invalid value! Answer only 1 or 2!')
		if choice == 1:
			while True:
				print()
				time.sleep(1)
				username = input('Provide your username: ').replace(" ", "")
				print()
				time.sleep(1)
				passwd = getpass.getpass('Provide your password: ').replace(" ", "")
				print()
				time.sleep(1)
				result = store_user(username, passwd)
				if result == True:
					print(colored('Your username and password was successfully stored! ', 'green'))
					print()
					return True, username
				if str(result) == f'1062 (23000): Duplicate entry \'{username}\' for key \'login.user\'':
					print(colored(f'There is already a user called {username}', 'red'))
		if choice == 2:
			while True:
				print()
				time.sleep(1)
				username = input('Provide your username: ').replace(" ", "")
				print()
				time.sleep(1)
				passwd = getpass.getpass('Provide your password: ').replace(" ", "")
				print()
				time.sleep(1)
				result = find_user(username, passwd)
				if str(result) == '\'NoneType\' object is not subscriptable': 
					text = f'The user {username} doesn\'t exist! Try again!'
					print(colored(text, 'red'))
				else:
					print(colored("Sucessfully logged! ", "green"))
					return True, username


def app():
	status, username = login()
	if status == True:
		blockchain = Blockchain()
		print()
		print('-' * 30 + f' Welcome to the Cryptocoin, {username}! ' + "-" * 30)
		while True:
			print()
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
				if choice <= 3 and choice > 0:
					break
				else:
					print()
					print(colored("Invalid value! Answer only 1, 2 or 3!", "red"))
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

						# Deleting the private key from the transaction for security purposes
						delattr(transaction, 'sender_private_key')

						Blockchain.add_transaction(public_transaction)
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
				print("Block mined and added to the successfully!")
				print()
				time.sleep(1)
				print("-" * 30)

			if choice == 3:
				return True
	else:
			print("Error during login")
			return False

if __name__ == '__main__':
	app()