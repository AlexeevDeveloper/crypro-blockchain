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
	coin_name="CPNC",
	max_supply=100.0,
	mining_reward=10.0,
	difficulty=0,
	consensus_algorithm=ConsensusAlgorithm.PROOF_OF_WORK,
	transaction_fee=1.5,
	inflation_rate=0.02,
	difficulty_update_time=60
)

blockchain = BlockChain(config)

wallet1 = blockchain.create_wallet('Alice', blockchain.max_supply // 4)
wallet2 = blockchain.create_wallet('Bob', 0.0)

blockchain.mine_block(wallet1)

tx1 = wallet1.send_transaction(wallet2, 9.5, blockchain.transaction_fee)

if tx1:
	blockchain.pending_transaction(tx1)
blockchain.mine_block(wallet2)

print('W1:', wallet1.balance)
print('W2:', wallet2.balance)

info = blockchain.get_full_info()

print(f'Текущее максимальное количество монет: {info["current_max_supply"]}')
print(f'Текущий отстаток монет в сети: {info["current_remaining_supply"]}')
print(f'Текущее общее количество монет во всех кошельках: {info["total_wallets_balance"]}')
print(f'Отношение текущего отстатка монет в сети к общему количеству монет во всех кошельках: {info["remaining_supply_percentage"]}')
print(f'Сложность майнинга и награда майнинга: {blockchain.config.difficulty}/{blockchain.config.mining_reward}')
print(f'Комиссия за транзакцию: {blockchain.transaction_fee}')
print(f'Рост инфляции: {blockchain.inflation_rate}')
print(f'Цепь: {blockchain.validate_chain()}')
