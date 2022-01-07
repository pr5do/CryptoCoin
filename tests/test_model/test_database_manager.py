from source.model.blockchain import generate_private_and_public_key
from source.model.database_manager import connect, store_public_key, store_user, find_user, delete_user, get_public_and_private_key_status, change_public_and_private_key_status, get_public_key, get_balance



# User Public Key
user_private, user_public = generate_private_and_public_key()
user_public = user_public.export_key(format='OpenSSH')

# Test username and password
username = 'TestDatabaseManager'
passwd = 'test1234'

def test_connect():
    connection = connect()

    assert connection.is_connected() == True


def test_store_user_and_delete_user():

    assert store_user(username, passwd) == True
    assert delete_user(username, passwd) == True


def test_find_user():

    store_user(username, passwd)

    assert find_user(username) == (username, passwd)

    delete_user(username, passwd)


def test_get_public_and_private_key_status():

    store_user(username, passwd)

    assert get_public_and_private_key_status(username) == 0
    assert get_public_and_private_key_status('Gustavo') == 1

    delete_user(username, passwd)


def test_store_public_key():

    public_key = user_public

    store_user(username, passwd)
    
    assert store_public_key(username, public_key) == True

    delete_user(username, passwd)


def test_change_public_and_private_key_status():

    store_user(username, passwd)

    assert change_public_and_private_key_status(username, 'I don\'t have a public key')[0] == True

    delete_user(username, passwd)


def test_get_public_key():

    public_key = user_public

    store_user(username, passwd)

    store_public_key(username, public_key)

    assert get_public_key(username) == public_key

    delete_user(username, passwd)

def test_get_balance():
    store_user(username, passwd)

    assert get_balance(username) == float(0)

    delete_user(username, passwd)

if __name__ == '__main__':
    test_store_user_and_delete_user()
