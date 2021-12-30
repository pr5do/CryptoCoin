from source.model.blockchain import generate_public_and_private_key, random_string_generator
from source.model.blockchain import Transaction, Blockchain, Block


def test_generate_public_and_private_key():
   
  private_key, public_key = generate_public_and_private_key()
  private_key2, public_key2 = generate_public_and_private_key()

  assert public_key != public_key2
  assert private_key != private_key2

  assert public_key.exportKey('PEM') != public_key2.exportKey('PEM')
  assert private_key.exportKey('PEM') != private_key2.exportKey('PEM')

  assert public_key.exportKey('PEM').decode('utf-8') != public_key2.exportKey('PEM').decode('utf-8')
  assert private_key.exportKey('PEM').decode('utf-8') != private_key2.exportKey('PEM').decode('utf-8')

def test_random_string_generator():

  password = random_string_generator()
  password2 = random_string_generator()

  assert password != password2 

# Transaction class testing

def test_sign_transaction():

  sender_private_key, sender_public_key = generate_public_and_private_key()
  recipient_private_key, recipient_public_key = generate_public_and_private_key()

  transaction = Transaction(sender_public_key, recipient_public_key, sender_private_key, 42)

  assert transaction.sign_transaction() != transaction.sign_transaction()

# Block class testing

def test_mining():

  data = "Programming is cool"
  index = 42
  prev_hash = "0" * 64

  block = Block(data, index, prev_hash)

  assert block.mining() == block.mining()

  data = "Hacking is cool"

  block2 = Block(data, index, prev_hash)

  assert block.mining() != block2.mining()

# Blockchain class testing

def test_add_transaction():
  blockchain = Blockchain()

  transaction = "Dave gives 10 cryptocoins to Alex"

  assert blockchain.add_transaction(transaction) == True

def test_construct_block():
  blockchain = Blockchain()

  transaction = "Boby gives 42 cryptocoins to Alex"

  blockchain.add_transaction(transaction)

  assert blockchain.current_data == [transaction]

  block = blockchain.construct_block()

  genesis = vars(blockchain)['chain'][0]

  assert blockchain.chain == [genesis, block]

def construct_genesis():
  blockchain = Blockchain()

  genesis = vars(blockchain)['chain'][0]

  assert blockchain.construct_genesis == True, genesis
