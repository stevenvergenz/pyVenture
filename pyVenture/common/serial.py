import abc
import types
import events

class Serial:
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	def deserialize(cls, dump, world = None):
	
		obj = None
		
		if cls == types.Player:
		
			obj = types.Player(dump['name'])
			obj.currentArea = world.areas[dump['currentArea']]
			
		elif cls == types.World:
		
			obj = types.World()
			for id, area in dump['areas'].items():
				obj.areas[id] = types.Area.deserialize(area, obj)
				obj.areas[id].id = id
				obj.areas[id].parentWorld = obj
				
			obj.player = types.Player.deserialize( dump['player'], obj )
		
		elif cls == types.Area:
		
			obj = types.Area(dump['name'], dump['entranceText'])
			for feature in dump['features']:
				obj.features.append( types.Feature.deserialize(feature, world) )
				obj.features[-1].parentArea = obj
				
		elif cls == types.Feature:
		
			obj = types.Feature(dump['name'], dump['description'])
			for action in dump['actions']:
				obj.actions.append( types.Action.deserialize(action, world) )
				obj.actions[-1].parentFeature = obj
				
		elif cls == types.Action:
		
			obj = types.Action(dump['description'])
			for event in dump['events']:
				obj.events.append( events.Event.deserialize(event, world) )
				
		else:
			print 'Problem class:', cls.__name__
			
		return obj
		
	@abc.abstractmethod
	def serialize(self):
		return {}
		
