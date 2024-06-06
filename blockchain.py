#!venv/bin/python3
"""CryPro-N Coin BlockChain
Простой блокчейн для криптовалюты $CPNC, написанный на Python
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
import ecdsa
from datetime import datetime
from hashlib import sha256
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import os
from time import time

# Настройка логирования #
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание директории для логов
log_dir = 'logs'
if not os.path.exists(log_dir):
	os.makedirs(log_dir)

# Создаем файловый обработчик
file_handler = logging.FileHandler(os.path.join(log_dir, f'blockchain-{time()}.log'))
file_handler.setLevel(logging.DEBUG)

# Создаем обработчик форматирования
formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
file_handler.setFormatter(formatter)

# Применяем настройки
logger.addHandler(file_handler)
# Конец настройки логирования #


class ConsensusAlgorithm(Enum):
	"""
	Перечисление доступных алгоритмов консенсуса.
	"""
	PROOF_OF_WORK: str = "proof_of_work"
	PROOF_OF_STAKE: str = "proof_of_stake"
	# TODO: Реализовать Proof of Stake


@dataclass
class BlockChainConfig:
	"""
	Конфигурация блокчейна
	"""
	coin_name: str
	total_supply: float
	decimal_places: int
	mining_reward: float = 10.0
	difficulty: int = 2
	consensus_algorithm: ConsensusAlgorithm = ConsensusAlgorithm.PROOF_OF_WORK


class Wallet:
	"""
	Кошелек
	"""
	def __init__(self, name: str, initial_balance: float=0.0) -> None:
		self.name = name
		self.balance = initial_balance
		self.private_key, self.public_key = self.generate_key_pair()
		logger.info(f'Created new wallet with public key: {self.public_key.to_string().hex()}; and balance: {self.balance}')

	def generate_key_pair(self) -> Tuple:
		privkey = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
		pubkey = privkey.get_verifying_key()

		return privkey, pubkey

	def sign_transaction(self, transaction: 'Transaction') -> bytes:
		return self.private_key.sign(transaction.to_bytes())

	def send_transaction(self, recipient: 'Wallet', amount: float) -> 'Transaction':
		if self.balance >= amount:
			transaction = Transaction(self.public_key, recipient.public_key, amount)
			transaction.sign(self)
			logger.info(f'Sent transaction: {transaction}')
			return transaction
		else:
			logger.warning(f'Insufficient funds to send transaction from wallet: {self.public_key.to_string().hex()}')
			return None

	def withdraw(self, amount: float):
		self.balance -= amount

	def receive_transaction(self, transaction) -> None:
		self.balance += transaction.amount


class Transaction:
	def __init__(self, sender_wallet: Wallet, recipient_wallet: Wallet, amount: float, timestamp: Optional[datetime]=None) -> None:
		self.sender_wallet = sender_wallet
		self.recipient_wallet = recipient_wallet
		self.amount = amount
		self.timestamp: datetime = timestamp or datetime.now()
		self.signature: Optional[bytes] = None

	def sign(self, wallet: Wallet) -> None:
		self.signature = wallet.sign_transaction(self)

	def to_bytes(self) -> bytes:
		return f'{self.sender_wallet},{self.recipient_wallet},{self.amount},{self.timestamp.isoformat()}'.encode()

	def __str__(self) -> str:
		return f'Transaction(sender={self.sender_wallet.to_string().hex()}, recipient={self.recipient_wallet.to_string().hex()},amount={self.amount},timestamp={self.timestamp})'


class Block:
	def __init__(self, index: int, transactions: List[Transaction], previous_hash: bytes, timestamp: Optional[datetime]=None, nonce: int=0) -> None:
		self.index: int = index
		self.transactions = transactions
		self.previous_hash = previous_hash
		self.timestamp = timestamp or datetime.now()
		self.nonce = nonce

	@property
	def hash(self) -> bytes:
		block_data = f'{self.index},{[t.to_bytes().decode() for t in self.transactions]},{self.previous_hash.hex()},{self.timestamp.isoformat()},{self.nonce}'.encode()
		return sha256(block_data).digest()

	def mine(self, difficulty: int) -> None:
		target: bytes = b"0" * difficulty

		logger.info(f'Mine block with difficulty {difficulty}')
		print(f'Mine block with difficulty {difficulty}...')

		while self.hash[:difficulty] != target:
			self.nonce += 1

		print('End of mining block!')


class BlockChain:
	def __init__(self, config: BlockChainConfig):
		self.config = config
		self.chain = [self.create_genesis_block()]
		self.unconfirmed_transactions: List[Transaction] = []
		self.wallets = list()

	def create_genesis_block(self) -> Block:
		return Block(0, [], str("0" * 64).encode(), datetime.now())

	def add_block(self, block: Block) -> bool:
		try:
			logger.info(f'New block added: {block.hash.hex()}')
			self.chain.append(block)
			return True
		except Exception as e:
			logger.error(f'New block {block.hash} was not added: {e}')
			return False

	def validate_chain(self) -> bool:
		try:
			for i in range(1, len(self.chain)):
				current_block = self.chain[i]
				previous_block = self.chain[i - 1]

				if current_block.previous_hash != previous_block.hash:
					return False

			return True
		except Exception:
			return False

	def mine_block(self, wallet: Wallet) -> bool:
		if self.config.consensus_algorithm == ConsensusAlgorithm.PROOF_OF_WORK:
			if self.unconfirmed_transactions:
				block = Block(len(self.chain), self.unconfirmed_transactions, self.chain[-1].hash)
				block.mine(self.config.difficulty)
				self.add_block(block)

				logger.info(f'Wallet {wallet.public_key.to_string().hex()} mined a new block: {block.hash.hex()}')

				if self.config.mining_reward <= self.config.total_supply:
					wallet.balance += self.config.mining_reward
				else:
					logger.error('The total_supply has ended, the reward has not been gived')
			else:
				logger.debug('No pending transactions to mine')
		else:
			logger.warning(f'Consensus algorithm {self.config.consensus_algorithm.value} is not implemented yet.')
			return None

	def create_wallet(self, name, initial_balance) -> Wallet:
		wallet = Wallet(name, initial_balance)
		self.wallets.append(wallet)

		logger.info(f'New wallet has been registered: {wallet.public_key.to_string().hex()}')

		return wallet

	def process_transaction(self, transaction) -> bool:
		sender_wallet = next((w for w in self.wallets if w.public_key == transaction.sender_wallet), None)
		recipient_wallet = next((w for w in self.wallets if w.public_key == transaction.recipient_wallet), None)
		
		if sender_wallet and recipient_wallet:
			logger.info(f'Transfer transaction: {transaction.amount} {self.config.coin_name} from {transaction.sender_wallet.to_string().hex()} -> {transaction.recipient_wallet.to_string().hex()}')
			sender_wallet.send_transaction(recipient_wallet, transaction.amount)
			sender_wallet.withdraw(transaction.amount)
			recipient_wallet.receive_transaction(transaction)

			self.unconfirmed_transactions.append(transaction)
			self.add_block(Block(len(self.chain), self.unconfirmed_transactions, self.chain[-1].hash))
			return True
		else:
			return False
