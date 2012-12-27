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
			obj.currentArea = world.areas[ world.areaLookup[dump['currentArea']] ]
			
		elif cls == types.World:
		
			obj = types.World()
			for area in dump['areas']:
				areaObj = types.Area.deserialize(area, obj)
				areaObj.parentWorld = world
				obj.areaLookup[area['id']] = len(obj.areas)
				obj.areas.append(types.Area.deserialize(area, obj))
				
			obj.player = types.Player.deserialize( dump['player'], obj )
		
		elif cls == types.Area:
		
			obj = types.Area(dump['name'], dump['entranceText'])
			obj.id = dump['id']
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
				newEvent = events.Event.deserialize(event,world)
				newEvent.parentAction = obj
				obj.events.append( newEvent )
				
		else:
			print 'Problem class:', cls.__name__
			
		return obj
		
	@abc.abstractmethod
	def serialize(self):
		return {}
		
