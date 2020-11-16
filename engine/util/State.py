class State:
	def __init__(self, name):
		self.name = name
		self.func = None
		self.funcArgs = None

	def tick(self):
		if self.func is None:
			raise NotImplementedError

		self.func(*self.funcArgs)

	def setFunc(self, func, *args):
		self.func = func
		self.funcArgs = args

	def getName(self):
		return self.name