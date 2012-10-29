
class Event:

	def __init__(self):
		self.type = 'Event'
		raise NotImplementedError('Cannot use Event class directly. Use a subclass instead')

	def __call__(self, actor, action):
		raise NotImplementedError('Cannot use Event class directly. Use a subclass instead')

	def serialize(self):
		return {}
		
# end class Event


class TextEvent(Event):

	def __init__(self, text):

		self.type = 'TextEvent'
		self.text = text

	def __call__(self, actor, action):
		print self.text

	def serialize(self):
		return {'type': self.type, 'text': self.text }
		
# end class TextEvent


class PlayerMoveEvent(Event):

	def __init__(self, destination):
		self.type = 'PlayerMoveEvent'
		self.destination = destination

	def __call__(self, actor, action):
		actor.currentArea = self.destination
		
	def serialize(self):
		return {'type': self.type, 'destination': self.destination.id}

# end class PlayerMoveEvent


