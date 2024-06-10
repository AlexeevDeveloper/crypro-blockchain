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
from dataclasses import dataclass
from enum import Enum


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
