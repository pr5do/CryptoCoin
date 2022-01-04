# Process needed to run the files on the /model folder
import sys
sys.path.insert(0, "C:/Users/gusta\OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

import getpass
import time 
from argon2 import PasswordHasher
from termcolor import colored
from database_manager import store_user, find_user
from argon2.exceptions import VerifyMismatchError
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