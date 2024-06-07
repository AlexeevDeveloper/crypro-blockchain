#!venv/bin/python3
"""CryPro-N Coin BlockChain
Невероятно быстрый, защищенный и простой Open Source блокчейн. 

CryProN (крайпрон) демонстрирует основные концепции технологии блокчейна, 
такие как транзакции, экономические модели, блоки, кошельки, механизмы
консенсуса и многое другое.

Copyright (C) 2024  Alexeev Bronislav

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
"""
from blockchain import BlockChainConfig, BlockChain, ConsensusAlgorithm


config = BlockChainConfig(
	coin_name="MyToken",
	total_supply=100.0,
	decimal_places=9,
	mining_reward=10.0,
	difficulty=1,
	consensus_algorithm=ConsensusAlgorithm.PROOF_OF_WORK
)

blockchain = BlockChain(config)

wallet1 = blockchain.create_wallet('Alice', 100.0)
wallet2 = blockchain.create_wallet('Bob', 0.5)

tx1 = wallet1.send_transaction(wallet2, 9.5)

if tx1:
	blockchain.pending_transaction(tx1)

blockchain.mine_block(wallet1)
blockchain.mine_block(wallet2)

print('W1:', wallet1.balance)
print('W2:', wallet2.balance)

if blockchain.validate_chain():
	print('YES')
else:
	print('NO')

print('Остаток монет в сети:', blockchain.get_remaining_supply())

for block in blockchain.chain:
	print('-----------')
	print(f'Блок #{block.index}')
	print(f'Время: {block.timestamp}')
	print(f'Хеш: {block.hash.hex()}')
	print(f'Хеш предыдущего блока: {block.previous_hash.hex()}')