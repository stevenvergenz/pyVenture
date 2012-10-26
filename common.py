class World:

	def __init__(self):

		self.areas = {}
		self.player = None

		
	def addArea(self, area):
	
		if not isinstance(area, Area):
			raise TypeError('Cannot add a non-area to the area list')
			
		area.id = _generateId(area)
		self.areas[area.id] = area
		
		
	def _generateId(self, area):

		i = 1
		while area.name + ' ' + str(i) in self.areas.keys():
			i += 1
		return area.name + ' ' + str(i)
			
	

class Area:

	def __init__(self, name, entranceDescription):
	
		self.name = name
		self.entranceDescription = entranceDescription
		self.features = []
		
# end class Area


class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.description = description
		self.actions = []
		
# end class Feature


class Passage(Feature):

	def __init__(self, name, description, destination):
	
		Feature.__init__(self, name, description)
		self.destination = destination
		
		# add the 'go through' action
		def travelThrough(actor):
			actor.moveTo(destination)
			
		travel = Action('Go through '+name, self, travelThrough)
		self.actions.append(travel)


class Action:

	def __init__(self, description, receiver, handler):
	
		self.description = description
		if isinstance(receiver, Feature):
			self.receiver = receiver
		else:
			raise TypeError('Action receiver must be a Feature')
		self.execute = handler
	
# end class Action


class Player:

	def __init__(self, name):
	
		self.name = name
		self.inventory = []
		
	def moveTo(self, destination):
	
		self.currentArea = destination
		print destination.entranceDescription
		
# end class Player
