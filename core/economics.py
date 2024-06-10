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
import math


class EconomicModel:
	def __init__(self, blockchain: 'BlockChain'):
		self.blockchain = blockchain
		self.target_inflation_rate = self.blockchain.config.inflation_rate
		self.target_transaction_fee = self.blockchain.config.transaction_fee

	def get_min_threshold(self) -> float:
		min_threshold = self.blockchain.transaction_fee / (1 - self.blockchain.inflation_rate) * self.blockchain.max_supply / self.blockchain.config.mining_reward
		min_threshold = min(0.15 * self.blockchain.max_supply, min(0.5 * self.blockchain.max_supply, min_threshold))

		return min_threshold

	def get_max_threshold(self) -> float:
		max_threshold = self.blockchain.transaction_fee / (1 - self.blockchain.inflation_rate) * self.blockchain.max_supply / self.blockchain.config.mining_reward
		max_threshold = max(0.85 * self.blockchain.max_supply, min(0.95 * self.blockchain.max_supply, max_threshold))

		return max_threshold

	def adjust_inflantion_rate(self, current_inflation: float) -> float:		
		adjusted_inflation = current_inflation

		if current_inflation > self.target_inflation_rate:
			inflation_difference = (current_inflation - self.target_inflation_rate) / 10
			adjusted_inflation = current_inflation - inflation_difference
		elif current_inflation < self.target_inflation_rate:
			inflation_difference = (self.target_inflation_rate - current_inflation) / 10
			adjusted_inflation = current_inflation + inflation_difference

		return adjusted_inflation

	def check_need_tokens(self, tolerance=0.1) -> bool:
		min_threshold_range = self.get_min_threshold() * (1 + tolerance)
		max_threshold_range = self.get_max_threshold() * (1 + tolerance)
		return self.blockchain.remaining_supply >= min_threshold_range and self.blockchain.remaining_supply <= max_threshold_range

	def manage_tokens(self):
		target_tokens = (self.get_min_threshold() + self.get_max_threshold()) / 2

		new_tokens = target_tokens - self.blockchain.remaining_supply

		while new_tokens > self.get_min_threshold() and new_tokens < self.get_max_threshold():
			if new_tokens > self.get_max_threshold():
				new_tokens = self.get_max_threshold() - self.blockchain.remaining_supply
			else:
				new_tokens = self.get_max_threshold() - self.blockchain.remaining_supply

		new_tokens = math.floor(new_tokens)

		self.blockchain.remaining_supply += new_tokens

		perc1 = (self.target_inflation_rate - self.blockchain.inflation_rate) / 100
		perc2 = (self.blockchain.inflation_rate - self.target_inflation_rate) / 100

		if perc1 == 0: perc1 = 0.001
		if perc2 == 0: perc2 = 0.001

		if new_tokens > 0:
			if self.blockchain.inflation_rate < self.target_inflation_rate:
				self.blockchain.inflation_rate += perc1
			else:
				self.blockchain.inflation_rate += perc2
		else:
			if self.blockchain.inflation_rate < self.target_inflation_rate:
				self.blockchain.inflation_rate -= perc1
			else:
				self.blockchain.inflation_rate -= perc2

		return new_tokens
