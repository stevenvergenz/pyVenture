import abc

import events

class Serial:
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	def deserialize(cls, dump, world = None):
	
		obj = None
		
		if cls == Player:
		
			obj = Player(dump['name'])
			obj.currentArea = world.areas[ world.areaLookup[dump['currentArea']] ]
			
		elif cls == World:
		
			obj = World()
			for area in dump['areas']:
				areaObj = Area.deserialize(area, obj)
				areaObj.parentWorld = obj
				obj.areaLookup[area['id']] = len(obj.areas)
				obj.areas.append(areaObj)
				
			obj.player = Player.deserialize( dump['player'], obj )
		
		elif cls == Area:
		
			obj = Area(dump['name'], dump['entranceText'])
			obj.id = dump['id']
			for feature in dump['features']:
				obj.features.append( Feature.deserialize(feature, world) )
				obj.features[-1].parentArea = obj
				
		elif cls == Feature:
		
			obj = Feature(dump['name'], dump['description'])
			for action in dump['actions']:
				obj.actions.append( Action.deserialize(action, world) )
				obj.actions[-1].parentFeature = obj
				
		elif cls == Action:
		
			obj = Action(dump['description'])
			for event in dump['events']:
				newEvent = events.Event.deserialize(event,world)
				newEvent.parentAction = obj
				obj.events.append( newEvent )
				
		else:
			print 'Problem class:', cls.__name__
			
		return obj
		
	@abc.abstractmethod
	def serialize(self):
		return {}


class World(Serial):

	def __init__(self):

		self.areas = []
		self.areaLookup = {}
		self.player = Player('Hero')
		
	def addArea(self, area, index = -1):
	
		if not isinstance(area, Area):
			raise TypeError('Cannot add a non-area to the area list')
		
		if self.player.currentArea == None:
			self.player.currentArea = area

		area.id = self._generateId(area)
		area.parentWorld = self
		if index >= 0:
			self.areas.insert(index, area)
			for key, idx in self.areaLookup.items():
				if idx >= index: self.areaLookup[key] = idx+1
			self.areaLookup[area.id] = index
		else:
			self.areaLookup[area.id] = len(self.areas)
			self.areas.append(area)

	def updateAreaIndex(self):

		self.areaLookup = {}
		for i,area in enumerate(self.areas):
			self.areaLookup[area.id] = i

	def _generateId(self, area):

		i = 1
		while area.name + ' ' + str(i) in self.areaLookup.keys():
			i += 1
		return area.name + ' ' + str(i)
		
	def serialize(self):
	
		dump = {}
		dump['areas'] = []
		for area in self.areas:
			dump['areas'].append(area.serialize())
			
		dump['player'] = self.player.serialize()
		
		return dump		


	def __eq__(self, other):

		if type(self) != type(other):
			return NotImplemented

		if (self.player != None and other.player != None) and self.player != other.player:
			return False

		for i,area in enumerate(self.areas):
			try:
				if area != other.areas[i]:
					return False
			except IndexError:
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
		dump['id'] = self.id
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
			self.events.append( events.TextEvent({'text':actionText}) )
		
	def trigger(self, actor):

		for consequent in self.events:
			status = consequent(actor, self)
			if status is not None:
				return status
			
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
