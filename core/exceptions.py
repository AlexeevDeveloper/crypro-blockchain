

class BlockChainException(Exception):
	"""
	Общее исключение для блокчейна, которое было удостоино вниманием.
	"""
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			return f'BlockChainException: {self.message}'
		else:
			return 'BlockChainException'
