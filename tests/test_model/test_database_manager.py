# Process needed to run the files on the /model folder
import sys
sys.path.insert(1, "C:/Users/gusta/OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from database_manager import connect, store_user, find_user, delete_user

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

