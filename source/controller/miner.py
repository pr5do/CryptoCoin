'''
# Previews mining protocol

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


'''