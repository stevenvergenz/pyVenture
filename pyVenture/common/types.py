import events
from serial import Serial

class World(Serial):

	def __init__(self):

		self.areas = {}
		self.player = Player('Hero')
		
	def addArea(self, area):
	
		if not isinstance(area, Area):
			raise TypeError('Cannot add a non-area to the area list')
		
		if self.player.currentArea == None:
			self.player.currentArea = area

		area.id = self._generateId(area)
		area.parentWorld = self
		self.areas[area.id] = area

	def updateArea(self, area):

		del self.areas[area.id]
		self.addArea(area)
		
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


	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		if (self.player != None and other.player != None) and self.player != other.player:
			return False

		for id,area in self.areas.items():
			if id not in other.areas or area != other.areas[id]:
				return False

		return True

	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result


# end class World


class Area(Serial):

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

	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		if self.name != other.name or self.entranceText != other.entranceText:
			return False

		if len(self.features) != len(other.features):
			return False

		for i in range(len(self.features)):
			if self.features[i] != other.features[i]:
				return False

		return True
		
	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result

# end class Area


class Feature(Serial):

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

	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		if self.name != other.name or self.description != other.description:
			return False

		if len(self.actions) != len(other.actions):
			return False

		for i in range(len(self.actions)):
			if self.actions[i] != other.actions[i]:
				return False

		return True

	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result

		
# end class Feature


class Action(Serial):

	def __init__(self, description, actionText = None):
		self.description = description
		self.parentFeature = None
		self.events = []
		if actionText != None:
			self.events.append( events.TextEvent(actionText) )
		
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
	
	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		if self.description != other.description:
			return False

		if len(self.events) != len(other.events):
			return False

		for i in range(len(self.events)):
			if self.events[i] != other.events[i]:
				return False

		return True

	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result


# end class Action


class Player(Serial):

	def __init__(self, name):
		self.name = name
		self.inventory = []
		self.currentArea = None
		
	def serialize(self):
	
		dump = {}
		dump['name'] = self.name
		dump['currentArea'] = self.currentArea.id if self.currentArea is not None else ''
		dump['inventory'] = []
		for i in self.inventory:
			dump['inventory'].append(i)

		return dump

	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		return True

	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result

# end class Player
