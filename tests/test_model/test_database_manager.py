# Process needed to run the files on the /model folder
import sys
sys.path.insert(0, "C:/Users/gusta/OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from database_manager import connect, store_public_key, store_user, find_user, delete_user, get_public_and_private_key_status, change_public_and_private_key_status
from blockchain import generate_private_and_public_key

# User Public Key
user_private, user_public = generate_private_and_public_key()
user_public = user_public.export_key(format='OpenSSH').split()[1]

def test_connect():
  connection = connect()

  assert connection.is_connected() == True


def test_store_user_and_delete_user():

  username = 'Test'
  passwd = 'test12345'

  assert store_user(username, passwd) == True
  assert delete_user(username, passwd) == True


def test_find_user():

  username = 'Test'
  passwd = 'test12345'

  store_user(username, passwd)

  assert find_user(username) == (username, passwd)

  delete_user(username, passwd)

def test_get_public_and_private_key_status():
  username = 'Test'
  passwd = 'test12345'

  store_user(username, passwd)

  assert get_public_and_private_key_status('Test') == (0,)
  assert get_public_and_private_key_status('Gustavo') == (1,)
  
  delete_user(username, passwd)


def test_store_public_key():
  username = 'Analice'
  passwd='1'

  store_user(username, passwd)
  assert store_public_key('Analice', user_public) == True

def test_change_public_and_private_key_status():
  assert change_public_and_private_key_status('Analice', user_public)[0] == False

  username = 'Test'
  passwd = 'test12345'

  store_user(username, passwd)

  assert change_public_and_private_key_status('Test', 'I don\'t have a public key')[0] == True
  
  delete_user(username, passwd)


