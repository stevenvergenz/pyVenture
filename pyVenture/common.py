class World:

	def __init__(self):

		self.areas = {}
		self.player = None

		
	def addArea(self, area):
	
		if not isinstance(area, Area):
			raise TypeError('Cannot add a non-area to the area list')
			
		area.id = self._generateId(area)
		self.areas[area.id] = area
		
		
	def _generateId(self, area):

		i = 1
		while area.name + ' ' + str(i) in self.areas.keys():
			i += 1
		return area.name + ' ' + str(i)
			
	

class Area:

	def __init__(self, name, entranceText):
	
		self.name = name
		self.entranceText = entranceText
		self.features = []
		
# end class Area


class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.description = description
		self.actions = []
		
# end class Feature


class Action:

	def __init__(self, description, actionText, parentFeature):
	
		self.type = 'Action'
		self.description = description
		self.actionText = actionText

		if isinstance(parentFeature, Feature):
			self.parentFeature = parentFeature
		else:
			raise TypeError('Action parent must be a Feature')

	def execute(self, actor):

		print self.actionText
	
# end class Action


class PlayerMoveAction(Action):

	def __init__(self, description, actionText, parentFeature, destination):

		Action.__init__(self, description, actionText, parentFeature)
		self.type = 'PlayerMoveAction'
		self.destination = destination

	def execute(self, actor):

		Action.execute(self, actor)
		actor.currentArea = self.destination

# end class PlayerMoveAction


class Player:

	def __init__(self, name):
	
		self.name = name
		self.inventory = []
		self.currentArea = None

# end class Player
