import abc				
from serial import Serial
	
class Event(Serial):
	__metaclass__ = abc.ABCMeta
	
	def __new__(cls, *args, **kwargs):
		instance = object.__new__(cls)
		instance.type = instance.__class__.__name__
		return instance
	
	@abc.abstractmethod
	def __call__(self, actor, action):
		"""Called when the parent action is triggered."""
		pass

		
	@staticmethod
	@abc.abstractmethod
	def deserialize(dump, world):
		pass
		
	@abc.abstractmethod
	def serialize(self):
		"""Serializes the event into a dictionary for file dumping."""
		return {}
		
# end class Event


class TextEvent(Event):

	def __init__(self, text):
		self.text = text

	def __call__(self, actor, action):
		print self.text

	def serialize(self):
		return {'type': self.type, 'text': self.text }
		
# end class TextEvent


class PlayerMoveEvent(Event):

	def __init__(self, destination):
		self.destination = destination

	def __call__(self, actor, action):
		actor.currentArea = self.destination
		
	def serialize(self):
		return {'type': self.type, 'destination': self.destination.id}

# end class PlayerMoveEvent


