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
from datetime import datetime
from hashlib import sha256
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import logging
import os
from time import time
import ecdsa

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

	На данный момент поддерживаются следующие виды механизма консенсуса:
	 + Proof of Work - алгоритм, в котором участники сети соревнуются в решении
	 	вычислительно-сложной задачи. Цель этой задачи - найти значение
	 	нонса, которое, когда объединено с другими данным блока, дает хеш,
	 	удолетворяющий определенному критерию сложности. Этот критерий
	 	обычно требует, чтобы хеш начинался с определенного кол-ва нулей.
	 + Proof of Stake - альтернативный алгоритм, в котором участники сети
	 	(валидаторы) ставят на кон (блокируют) свои токены, чтобы иметь 
	 	право добавлять новые блоки в блокчейн. Вместо вычислительной мощи, PoS
	 	использует долю в сети (кол-во заблокированных токенов) для определения,
	 	кто должен добавить следующий блок.
	"""
	PROOF_OF_WORK: str = "proof_of_work"
	PROOF_OF_STAKE: str = "proof_of_stake"


class TransactionStatus(Enum):
	"""
	Статус транзакции.

	 + PENDING/в обработке - 1
	 + CONFIRMED/подтвержден - 2
	 + FAILED/провал - 3
	"""
	PENDING = 1
	CONFIRMED = 2
	FAILED = 3


@dataclass
class BlockChainConfig:
	"""
	Конфигурация блокчейна.

	Параметры:
	 + Название монеты
	 + Общее количество выпущенных монет
	 + Награда для майнеров
	 + Сложность добычи блоков
	 + Алгоритм консенсуса
	 + Комиссия за транзакцию
	 + Рост инфляции
	 + Максимальное время добычи блока для обновления сложности (в секундах)
	"""
	coin_name: str
	max_supply: float
	mining_reward: float = 10.0
	difficulty: int = 2
	consensus_algorithm: ConsensusAlgorithm = ConsensusAlgorithm.PROOF_OF_WORK
	transaction_fee: float = 1.0
	inflation_rate: float = 0.02
	difficulty_update_time: int = 60


class Wallet:
	"""
	Класс, представляющий собой криптовалютный кошелек в блокчейне.

	Каждый кошелек имеет:
	 + Имя владельца
	 + Начальный баланс
	 + Приватный и публичный ключ
	 + История транзакций
	"""
	def __init__(self, name: str, initial_balance: float=0.0) -> None:
		"""
		Инициализация кошелька

		:param name: Имя владельца
		:param initial_balance: Начальный баланс
		"""
		self.name: str = name
		self.balance: float = initial_balance
		self.private_key, self.public_key = self.generate_key_pair()
		self.transactions_history: Dict = {}
		logger.info(f'Created new wallet with public key: {self.public_key.to_string().hex()}; and balance: {self.balance}')

	def generate_key_pair(self) -> Tuple:
		"""
		Метод для генерации пары ключей (приватный и публичный)

		Данный метод задействует кривую NIST256p

		:return: Возвращает кортеж из приватного и публичного ключей
		"""
		privkey = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
		pubkey = privkey.get_verifying_key()

		return privkey, pubkey

	def sign_transaction(self, transaction: 'Transaction') -> bytes:
		"""
		Метод для подписи транзакции приватным ключем

		:param transaction: Транзакция

		:return: Подпись
		"""
		return self.private_key.sign(transaction.to_bytes())

	def send_transaction(self, recipient: 'Wallet', amount: float, fee: float) -> 'Transaction':
		"""
		Метод для отправки транзакции до получателя.

		Данный метод проверяет наличие средств на балансе и возвращает подписанную транзакцию.

		:param recipient: Кошелек получателя
		:param amount: Сумма транзакции

		:return: Подписанная транзакция
		"""
		if self.balance >= amount + fee:
			self.withdraw(amount + fee)
			transaction = Transaction(self.public_key, recipient.public_key, amount, fee)
			transaction.sign(self)
			logger.info(f'Send transaction: {transaction}')
			return transaction
		elif self.balance >= amount and self.balance < amount + fee:
			logger.warning(f'Insufficient funds to pay comission to send transaction from wallet: {self.public_key.to_string().hex()}')
			return None
		else:
			logger.warning(f'Insufficient funds to send transaction from wallet: {self.public_key.to_string().hex()}')
			return None

	def withdraw(self, amount: float) -> None:
		"""
		Вспомогательный метод для снятия денег с баланса

		:param amount: Сумма средств для снятия
		"""
		logger.debug(f'Withdraw amount {amount} from wallet {self.public_key.to_string().hex()}')
		self.balance -= amount

	def receive_transaction(self, transaction: 'Transaction') -> None:
		"""
		Вспомогательный метод для получения транзакции

		:param transaction: Транзакция
		"""
		logger.debug(f'Receive amount {transaction.amount} from wallet {self.public_key.to_string().hex()}')
		self.balance += transaction.amount


class Transaction:
	"""Класс, представляющий собой транзакцию в блокчейне.

	Каждая транзакция имеет:
	 + Публичный ключ отправителя
	 + Публичный ключ получателя
	 + Сумма средств
	 + Метка времени
	 + Сигнатура
	 + Комиссия за перевод внутри сети
	 + Статус транзакции
	 + Комиссия за транзакцию
	"""
	def __init__(self, sender_wallet: bytes, recipient_wallet: bytes, 
				amount: float, fee: float, timestamp: Optional[datetime]=None) -> None:
		"""
		Инициализация транзакции

		:param sender_wallet: Публичный ключ кошелька отправителя
		:param recipient_wallet: Публичный ключ кошелька получателя
		:param amount: Сумма средств
		:param fee: Комиссия
		:param timestamp: Метка времени
		"""
		self.sender_wallet: bytes = sender_wallet
		self.recipient_wallet: bytes = recipient_wallet
		self.amount: float = amount
		self.fee: float = fee
		self.timestamp: datetime = timestamp or datetime.now()
		self.signature: Optional[bytes] = None
		self.status = TransactionStatus.PENDING
		logger.debug(f'Create new transaction: {self.sender_wallet.to_string().hex()} -> {self.recipient_wallet.to_string().hex()}')

	def sign(self, wallet: Wallet) -> None:
		"""
		Метод для создания сигнатуры путем подписи транзакции

		:param wallet: Кошелёк пользователя
		"""
		logger.info(f'Sign transaction by {wallet.public_key.to_string().hex()}')
		self.signature = wallet.sign_transaction(self)

	def to_bytes(self) -> bytes:
		"""
		Метод для перевода транзакции в байты

		:return: Байты
		"""
		return f'{self.sender_wallet},{self.recipient_wallet},{self.amount},{self.timestamp.isoformat()}'.encode()

	def __str__(self) -> str:
		"""Строковое представление транзакции"""
		return f'Transaction(sender={self.sender_wallet.to_string().hex()}, recipient={self.recipient_wallet.to_string().hex()},amount={self.amount},timestamp={self.timestamp})'


class Block:
	"""
	Класс, представляющий собой блок в блокчейне.

	Каждый блок имеет:
	 + Индекс
	 + Список транзакций
	 + Хеш предыдущего блока
	 + Мета-данные
	 + Метка времени
	 + Специальное число nonce (для PoW)
	"""
	def __init__(self, index: int, transactions: List[Transaction], previous_hash: bytes, 
				metadata: Dict=None, timestamp: Optional[datetime]=None, nonce: int=0) -> None:
		"""
		Инициализация блока

		:param index: Индекс блока
		:param transactions: Список транзакций
		:param previous_hash: Хеш предыдущего блока
		:param metadata: Мета-данные в произвольном формате
		:param timestamp: Метка времени
		:param nonce: Спец.число Nonce
		"""
		self.index: int = index
		self.transactions: List[Transaction] = transactions
		self.previous_hash: bytes = previous_hash
		self.timestamp: datetime = timestamp or datetime.now()
		self.nonce: int = nonce
		self.metadata: Dict = metadata
		logger.debug(f'Created new block with timestamp {self.timestamp} and index {self.index}')

	@property
	def hash(self) -> bytes:
		"""
		Свойство класса для генерации хеша.

		:return: Хеш блока в виде байтов
		"""
		block_data = f'{self.index},{[t.to_bytes().decode() for t in self.transactions]},{self.previous_hash.hex()},{self.metadata},{self.timestamp.isoformat()},{self.nonce}'.encode()
		return sha256(block_data).digest()

	def mine(self, difficulty: int) -> None:
		"""
		Метод добычи блока.

		Генерирует бесконечно хеши, пока в начале не будет кол-во нулей,
		равной сложности добычи

		:param difficulty: Сложность добычи, т.е кол-во нулей в начале хеша
		"""
		target: bytes = b"0" * difficulty

		logger.info(f'Mine block{self.index} with difficulty {difficulty}')
		print(f'Mine block with difficulty {difficulty}...')

		while self.hash[:difficulty] != target:
			self.nonce += 1

		logger.info(f'End of mining block{self.index}!')
		print('End of mining block!')


class BlockChain:
	"""
	Класс, представляющий собой блокчейн.

	Каждый блокчейн имеет следующие параметры:
	 + Конфигурация блокчейна
	 + Список блоков (цепь)
	 + Список неподтвержденных транзакций
	 + Список кошельков, участвующих в сети
	 + Остаток монет в сети
	 + Максимальное количество монет
	 + Количество намайненных монет
	 + Рост инфляции
	 + Комиссия за транзакцию
	 + Последнее время добычи блока
	"""
	def __init__(self, config: BlockChainConfig) -> None:
		"""
		Инициализация блокчейна

		:param config: Конфигурация блокчейна
		"""
		self.config: BlockChainConfig = config
		self.chain: list = [self.create_genesis_block()]
		self.pending_transactions: List[Transaction] = []
		self.wallets: list = list()
		self.remaining_supply: float = self.config.max_supply
		self.max_supply: float = self.config.max_supply
		self.transaction_fee: float = self.config.transaction_fee
		self.inflation_rate: float = self.config.inflation_rate
		self.total_mined_coins: int = 0
		self.last_update_time = datetime.now()

	def create_genesis_block(self) -> Block:
		"""
		Создание начально, genesis-блока в блокчейне.

		:return: Блок с хешем из 64 нуля
		"""
		logger.debug('Create genesis block for blockchain')
		return Block(0, [], str("0" * 64).encode(), datetime.now())

	def add_block(self, block: Block) -> bool:
		"""
		Метод, отвечающий за добавление блока в блокчейн

		:param block: Новый блок

		:return: True в случае успеха, в противном случае False
		"""
		try:
			logger.info(f'New block added: {block.hash.hex()}')
			self.chain.append(block)
			return True
		except Exception as e:
			logger.error(f'New block {block.hash} was not added: {e}')
			return False

	def mine_block(self, wallet: Wallet) -> bool:
		"""
		Добыча блока пользователем на определенный кошелёк.

		:param wallet: Кошелёк майнера (или для получения вознаграждения)

		:return: True в случае успешной добычи, False в противном случае
		"""
		if self.config.consensus_algorithm == ConsensusAlgorithm.PROOF_OF_WORK:
			# Если механизм консенсуса - PoW
			if self.remaining_supply <= self.config.mining_reward:
				print('Error: no enough coins for pay mining reward')
				logger.error('No enough coins for pay mining_reward')
				return False

			if self.pending_transactions:
				block = Block(len(self.chain), self.pending_transactions, 
							self.chain[-1].hash, metadata={
								'account': wallet.public_key.to_string().hex(),
								'action': 'mine'
							}
				)
				
				block.mine(self.config.difficulty)
				
				self.add_block(block)

				logger.info(f'Wallet {wallet.public_key.to_string().hex()} mined a new block: {block.hash.hex()}')

				self.total_mined_coins += self.config.mining_reward
				wallet.balance += self.config.mining_reward

				self.remaining_supply -= self.config.mining_reward

				self.set_remaining_supply()
				self.update_mining_settings()
			else:
				logger.debug('No pending transactions to mine')
		else:
			# Если механизм консенсуса какой-то другой
			logger.warning(f'Consensus algorithm {self.config.consensus_algorithm.value} is not implemented yet.')
			return None

	def update_mining_settings(self) -> None:
		"""
		Обновление настроек майнинга - награды и сложности.

		Вознаграждение майнера меняется по следующему алгоритму:
		 1. Вычисляется влияние инфляции на награду
		 2. Из награждения минусуется влияние деленное на общее количество добытых монет

		Сложность меняется по следующему алгоритму:
		 1. Вычисляется прошедшее время - из текущего времени отнимается время 
		 	последнего обновления. Переводится в секунды.
		 2. Если прошедшее время меньше чем заданное время для обновления сложности,
		 	то сложность увеличивается на 1.
		 3. Если сложность заняла больше времени, чем положено, то сложность,
		 	наоборот, уменьшается
		"""
		tokens = self.config.mining_reward * self.config.inflation_rate
		self.config.mining_reward -= tokens / self.total_mined_coins

		logger.debug(f'Update miner reward. Current mining reward = {self.config.mining_reward}')

		elapsed_time = (datetime.now() - self.last_update_time).total_seconds()
		self.last_update_time = datetime.now()

		if elapsed_time < self.config.difficulty_update_time:
			self.config.difficulty += 1
			logger.debug(f'Update difficulty (+1). Current difficulty = {self.config.difficulty}')
		elif elapsed_time > self.config.difficulty_update_time:
			self.config.difficulty = max(self.config.difficulty - 1, 1)
			logger.debug(f'Update difficulty. Current difficulty = {self.config.difficulty}')

	def create_wallet(self, name: str, initial_balance: float) -> Wallet:
		"""
		Создание кошелька и его регистрация в блокчейне.

		:param name: Имя носителя кошелька
		:initial_balance: Начальный баланс на кошельке

		:return: Новый зарегистрированный кошелёк
		"""
		wallet: Wallet = Wallet(name, initial_balance)

		if wallet.balance > self.remaining_supply:
			logger.critical('Impossible to register a wallet: the initial balance exceeds remaining tokens in network.')
			return None
		else:
			self.remaining_supply -= wallet.balance
			self.set_remaining_supply()

		self.wallets.append(wallet)

		logger.info(f'New wallet has been registered: {wallet.public_key.to_string().hex()}')

		return wallet

	def pending_transaction(self, transaction: Transaction) -> bool:
		"""
		Метод для завершения транзакций.

		Мы получаем публичные ключи отправителя и получателя, после 
		отправляем сумму на баланс получателю

		После мы добавляем транзакцию в список ожидающих завершения транзакций
		и добавляем новый блок в блокчейн.

		:param transaction: Транзакция

		:return: True в случае существования отправителя и получателя, иначе False
		"""
		sender_wallet = next((w for w in self.wallets if w.public_key == transaction.sender_wallet), None)
		recipient_wallet = next((w for w in self.wallets if w.public_key == transaction.recipient_wallet), None)
		
		if sender_wallet and recipient_wallet:
			logger.info(f'Transfer transaction: {transaction.amount} {self.config.coin_name} from {transaction.sender_wallet.to_string().hex()} -> {transaction.recipient_wallet.to_string().hex()}')
			recipient_wallet.receive_transaction(transaction)
			self.remaining_supply += transaction.fee

			self.pending_transactions.append(transaction)
			self.add_block(Block(len(self.chain), 
							self.pending_transactions, 
							self.chain[-1].hash,
							metadata={
								'account': sender_wallet.public_key.to_string().hex(),
								'action': 'transfer',
								'recipient': recipient_wallet.public_key.to_string().hex()
							}))
			transaction.status = TransactionStatus.CONFIRMED
			self.get_wallet(sender_wallet.public_key).transactions_history[f'{transaction.signature.hex()}'] = {
				'recipient': recipient_wallet.public_key,
				'status': transaction.status
			}
			self.set_remaining_supply()
			return True
		else:
			logger.warning(f'FAILED | Transfer transaction is failed: {transaction.amount} {self.config.coin_name} from {transaction.sender_wallet.to_string().hex()} -> {transaction.recipient_wallet.to_string().hex()}')
			transaction.status = TransactionStatus.FAILED
			self.get_wallet(sender_wallet.public_key).transactions_history[f'{transaction.signature.hex()}'] = {
				'recipient': recipient_wallet.public_key,
				'status': transaction.status
			}
			return False

	def validate_chain(self) -> bool:
		"""
		Метод проверки цепи блоков.

		Сверяется предыдущий хеш текущего блока и хеш предыдущего блока.

		:return: True если цепь валидна, False в противном случае
		"""
		try:
			for i in range(1, len(self.chain)):
				current_block = self.chain[i]
				previous_block = self.chain[i - 1]

				if current_block.previous_hash != previous_block.hash:
					return False

			logger.debug('Validating chain: no errors')

			return True
		except Exception as ex:
			logger.error(f'Error when validate chain: {ex}')
			return False

	def set_remaining_supply(self) -> None:
		"""
		Метод для получения остатка невыпущенных монет в сети блокчейна

		:return: Остаток монет
		"""
		transaction_supply = sum(tx.amount for block in self.chain for tx in block.transactions)
		total_supply = self.max_supply - transaction_supply
		new_tokens = total_supply * self.inflation_rate
		inflation_fee = self.transaction_fee * self.inflation_rate

		self.max_supply += new_tokens
		self.remaining_supply += new_tokens
		self.transaction_fee += inflation_fee

	def get_full_info(self) -> dict:
		"""
		Получение некоторой информации о блокчейне.

		Возвращает список из текущего максимального числа монет, текущего
		остатка монет в сети, общий баланс всех кошельков и процент
		соотношения остатка монет в сети к общему балансу всех кошельков.
		"""
		total_wallets_balance: int = 0

		for wallet in self.wallets:
			total_wallets_balance += wallet.balance

		remaining_supply = self.max_supply - total_wallets_balance
		remaining_supply_percentage = (remaining_supply / self.max_supply) * 100

		return {
			'current_max_supply': self.max_supply,
			'current_remaining_supply': self.remaining_supply,
			'total_wallets_balance': total_wallets_balance,
			'remaining_supply_percentage': remaining_supply_percentage,
		}

	def get_wallet(self, public_key: bytes) -> Wallet:
		"""
		Получение кошелька в блокчейне по его публичному ключу.

		:param public_key: Публичный ключ кошелька

		:return: Кошелёк, либо None
		"""
		for wallet in self.wallets:
			if wallet.public_key == public_key:
				return wallet

		return None
