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
			
	def serialize(self):
	
		dump = {}
		dump['areas'] = {}
		for id,area in self.areas.items():
			dump['areas'][id] = area.serialize()
			
		dump['player'] = self.player.serialize()
		
		return dump
	
# end class World


class Area:

	def __init__(self, name, entranceText):
	
		self.name = name
		self.parentWorld = None
		self.entranceText = entranceText
		self.features = []
		
	def serialize(self):
	
		dump = {}
		dump['name'] = self.name
		dump['entranceText'] = self.entranceText
		dump['features'] = []
		for feature in self.features:
			dump['features'].append( feature.serialize() )
		
		return dump
		
# end class Area


class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.description = description
		self.parentArea = None
		self.actions = []
		
	def serialize(self):
	
		dump = {}
		dump['name'] = self.name
		dump['description'] = self.description
		dump['actions'] = []
		for action in self.actions:
			dump['actions'].append( action.serialize() )

		return dump
		
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
			
	def serialize(self):
	
		dump = {}
		dump['description'] = self.description
		dump['events'] = []
		for event in self.events:
			dump['events'].append( event.serialize() )
		
		return dump
	
# end class Action


class Player:

	def __init__(self, name):
	
		self.name = name
		self.inventory = []
		self.currentArea = None
		
	def serialize(self):
	
		dump = {}
		dump['name'] = self.name
		dump['currentArea'] = self.currentArea.id
		dump['inventory'] = []
		for i in self.inventory:
			dump['items'].append(i)

		return dump

# end class Player
