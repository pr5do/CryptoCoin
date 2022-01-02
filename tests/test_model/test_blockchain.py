# Process needed to run the files on the /model folder
import sys
sys.path.insert(1, "C:/Users/gusta/OneDrive/Software/Meus-Projetos/CryptoCoin/source/model")

from blockchain import generate_private_and_public_key, verify_transaction
from blockchain import Transaction, Blockchain, Block


def test_generate_private_and_public_key():
   
  private_key, public_key = generate_private_and_public_key()
  private_key2, public_key2 = generate_private_and_public_key()

  print(f"Public Key Exported: {public_key.export_key(format='PEM')}")
  print(f"Private Key Exported: {private_key.export_key(format='PEM')}")

  assert public_key != public_key2
  assert private_key != private_key2

  assert public_key.export_key(format='PEM') != public_key2.export_key(format='PEM')
  assert private_key.export_key(format='PEM') != private_key2.export_key(format='PEM')


# Transaction class testing

def test_sign_transaction():

  sender_private_key, sender_public_key = generate_private_and_public_key()
  recipient_private_key, recipient_public_key = generate_private_and_public_key()

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

def test_verify_transaction():
  sender_private, sender_public = generate_private_and_public_key()
  recipient_private, recipient_public = generate_private_and_public_key()

  transaction = Transaction(sender_public, recipient_public, sender_private, 11)

  public_transaction = transaction.sign_transaction()

  assert verify_transaction(public_transaction)[0] == True
