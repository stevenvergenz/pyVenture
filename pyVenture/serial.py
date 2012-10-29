import abc
import common
import events

class Serial:
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	def deserialize(cls, dump, world = None):
	
		obj = None
		
		if cls == common.World:
		
			obj = World()
			for id, area in dump['areas'].items():
				obj.areas[id] = Area.deserialize(area, obj)
				obj.areas[id].parentWorld = self
				
			obj.player = Player( self, dump['player'] )
		
		elif cls == common.Area:
		
			obj = Area(dump['name'], dump['entranceText'])
			for feature in dump['features']:
				obj.features.append( Feature.deserialize(feature, world) )
				obj.features[-1].parentArea = obj
				
		elif cls == common.Feature:
		
			obj = Feature(dump['name'], dump['description'])
			for action in dump['actions']:
				obj.actions.append( Action.deserialize(action, world) )
				obj.actions[-1].parentFeature = obj
				
		elif cls == common.Action:
		
			obj = Action(dump['description'])
			for event in dump['events']:
				obj.events.append( events.deserialize(dump) )
				
		elif cls == events.Event:
		
			for subclass in Event.__subclasses__():
				if subclass.__class__.__name__ == dump['type']:
					return subclass.deserialize(world, dump)
			
		return obj
		
	@abc.abstractmethod
	def serialize(self):
		return {}
		