# Process needed to run the files on the /model folder
import sys
sys.path.insert(0, "C:/Users/gusta\OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from blockchain import Blockchain, Transaction, generate_private_and_public_key
from database_manager import change_public_and_private_key_status, store_public_key, store_user, find_user, get_public_and_private_key_status
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from termcolor import colored
import getpass
import time
import os


def login():
    os.system('cls||clear')
    while True:
        print()
        ph = PasswordHasher()
        print("-" * 35)
        time.sleep(1)
        print()
        print('Choose between the options below: ')
        print()
        time.sleep(1)
        print('[1]: I don\'t have an account')
        time.sleep(1)
        print('[2]: I already have an account')
        print()
        time.sleep(1)
        print("-" * 35)
        time.sleep(1)
        while True:
            print()
            choice = int(getpass.getpass('Type: '))
            if choice <= 2 and choice > 0:
                break
            else:
                print()
                print(colored('Invalid value! Answer only 1 or 2!', 'red'))
        if choice == 1:
            while True:
                print()
                time.sleep(1)
                print("-" * 35)
                print()
                username = input('Provide your username: ').replace(" ", "")
                print()
                time.sleep(1)
                passwd = getpass.getpass('Provide your password: ').replace(" ", "")
                print()
                print("-" * 35)
                print()
                time.sleep(1)
                passwd = ph.hash(passwd)
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
                print("-" * 35)
                print()
                username = input('Provide your username: ').replace(" ", "")
                print()
                time.sleep(1)
                passwd = getpass.getpass('Provide your password: ').replace(" ", "")
                print()
                print("-" * 35)
                print()
                time.sleep(1)

                result = find_user(username)

                if str(result) == '\'NoneType\' object is not subscriptable':
                    text = f'The user {username} doesn\'t exist! Try again!'
                    print(colored(text, 'red'))

                try:
                    verify = ph.verify(result[1], passwd)
                except (VerifyMismatchError):
                    print(colored("Your password isn\'t correct!", "red"))
                except (TypeError):
                    verify = False

                try:
                    if verify == True:
                        print(colored("Sucessfully logged! ", "green"))
                        time.sleep(1)
                        return True, username
                except (UnboundLocalError):
                    pass


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
						# This is temporily commented because, for now, doesn't work, and I need to take a break
						'''
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
												private_key, public_key = generate_private_and_public_key()
												time.sleep(1)
												print(f"Your public key: {public_key.export_key(format='PEM')}")
												time.sleep(1)
												print()
												print(f"Your private key: {private_key.export_key(format='PEM')}")
												time.sleep(1)
												answer = "y"
											'''
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
