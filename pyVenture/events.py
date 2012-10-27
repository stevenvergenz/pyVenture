
class Event:

	def __init__(self):
		self.type = 'Event'
		raise NotImplementedError('Cannot use Event class directly. Use a subclass instead')

	def __call__(self, actor, action):
		raise NotImplementedError('Cannot use Event class directly. Use a subclass instead')

# end class Event


class TextEvent(Event):

	def __init__(self, text):

		self.type = 'TextEvent'
		self.text = text

	def __call__(self, actor, action):
		print self.text

# end class TextEvent


class PlayerMoveEvent(Event):

	def __init__(self, destination):
		self.type = 'PlayerMoveEvent'
		self.destination = destination

	def __call__(self, actor, action):
		actor.currentArea = self.destination

# end class PlayerMoveEvent


