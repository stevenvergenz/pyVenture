from events import TextEvent

class World:

	def __init__(self):

		self.areas = {}
		self.player = None

		
	def addArea(self, area):
	
		if not isinstance(area, Area):
			raise TypeError('Cannot add a non-area to the area list')
			
		area.id = self._generateId(area)
		area.parentWorld = self
		self.areas[area.id] = area
		
		
	def _generateId(self, area):

		i = 1
		while area.name + ' ' + str(i) in self.areas.keys():
			i += 1
		return area.name + ' ' + str(i)
			
	

class Area:

	def __init__(self, name, entranceText):
	
		self.name = name
		self.parentWorld = None
		self.entranceText = entranceText
		self.features = []
		
# end class Area


class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.description = description
		self.parentArea = None
		self.actions = []
		
# end class Feature


class Action:

	def __init__(self, description, actionText):
	
		self.description = description
		self.parentFeature = None
		self.events = []
		
		self.events.append( TextEvent(actionText) )

	def trigger(self, actor):

		for consequent in self.events:
			consequent(actor, self)
	
# end class Action


class Player:

	def __init__(self, name):
	
		self.name = name
		self.inventory = []
		self.currentArea = None

# end class Player
