import abc
import common
import events

class Serial:
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	def deserialize(cls, dump, world = None):
	
		obj = None
		
		if cls == common.Player:
		
			obj = common.Player(dump['name'])
			obj.currentArea = world.areas[dump['currentArea']]
			
		elif cls == common.World:
		
			obj = common.World()
			for id, area in dump['areas'].items():
				obj.areas[id] = common.Area.deserialize(area, obj)
				obj.areas[id].parentWorld = obj
				
			obj.player = common.Player.deserialize( dump['player'], obj )
		
		elif cls == common.Area:
		
			obj = common.Area(dump['name'], dump['entranceText'])
			for feature in dump['features']:
				obj.features.append( common.Feature.deserialize(feature, world) )
				obj.features[-1].parentArea = obj
				
		elif cls == common.Feature:
		
			obj = common.Feature(dump['name'], dump['description'])
			for action in dump['actions']:
				obj.actions.append( common.Action.deserialize(action, world) )
				obj.actions[-1].parentFeature = obj
				
		elif cls == common.Action:
		
			obj = common.Action(dump['description'])
			for event in dump['events']:
				obj.events.append( events.Event.deserialize(event, world) )
				
		elif cls == events.Event:
		
			for subclass in events.Event.__subclasses__():
				if subclass.__class__.__name__ == dump['type']:
					return subclass.deserialize(dump, world)
		else:
			print cls.__name__
			
		return obj
		
	@abc.abstractmethod
	def serialize(self):
		return {}
		