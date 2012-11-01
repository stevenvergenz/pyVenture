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

	def __init__(self, properties):
		self.properties = properties
	
	@abc.abstractmethod
	def __call__(self, actor, action):
		"""Called when the parent action is triggered."""
		pass

	@staticmethod
	def deserialize(dump, world):
		"""Populates a new event object with the contents of dump."""
		for subclass in itersubclasses(Event):
			if subclass.__name__ == dump['type']:
				del dump['type']
				return subclass(dump)
		
	def serialize(self):
		"""Serializes the event into a dictionary for file dumping."""
		return {'type': self.type} + self.properties
		
# end class Event


class TextEvent(Event):

	def __init__(self, properties):
		Event.__init__(self, properties)

	def __call__(self, actor, action):
		print self.properties['text']

# end class TextEvent


class PlayerMoveEvent(Event):

	def __init__(self, properties):
		Event.__init__(self, properties)

	def __call__(self, actor, action):
		actor.currentArea = action.parentFeature.parentArea.parentWorld.areas[ self.properties['destination'] ]
		
# end class PlayerMoveEvent


