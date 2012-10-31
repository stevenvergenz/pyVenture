import abc				
from serial import Serial

def itersubclasses(cls, _seen=None):
	"""
	itersubclasses(cls)

	Generator over all subclasses of a given class, in depth first order.
	Code written by Gabriel Genellina on ActiveState.com
	"""
	
	if not isinstance(cls, type):
		raise TypeError('itersubclasses must be called with '
						'new-style classes, not %.100r' % cls)
	if _seen is None: _seen = set()
	try:
		subs = cls.__subclasses__()
	except TypeError: # fails only when cls is type
		subs = cls.__subclasses__(cls)
	for sub in subs:
		if sub not in _seen:
			_seen.add(sub)
			yield sub
			for sub in itersubclasses(sub, _seen):
				yield sub


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
		"""Populates a new event object with the contents of dump."""
		for subclass in itersubclasses(Event):
			if subclass.__name__ == dump['type']:
				return subclass.deserialize(dump, world)
		
	@abc.abstractmethod
	def serialize(self):
		"""Serializes the event into a dictionary for file dumping."""
		return {}
		
# end class Event


class TextEvent(Event):

	def __init__(self, text):
		self.properties = {}
		self.properties['text'] = text

	def __call__(self, actor, action):
		print self.properties['text']

	def serialize(self):
		return {'type': self.type, 'text': self.properties['text'] }
		
	@staticmethod
	def deserialize(dump, world):
		return TextEvent(dump['text'])

# end class TextEvent


class PlayerMoveEvent(Event):

	def __init__(self, destination):
		self.properties = {}
		self.properties['destination'] = destination

	def __call__(self, actor, action):
		actor.currentArea = action.parentFeature.parentArea.parentWorld.areas[ self.properties['destination'] ]
		
	def serialize(self):
		return {'type': self.type, 'destination': self.properties['destination']}
	
	@staticmethod
	def deserialize(dump, world):
		return PlayerMoveEvent( dump['destination'] )

# end class PlayerMoveEvent


