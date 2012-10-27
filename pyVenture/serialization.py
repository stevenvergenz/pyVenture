import common
import json


def serializeWorld(world):

	if world == None:
		return '{}'
	else:
		dump = {}
		
	dump['areas'] = {}
	for k,v in world.areas.items():
		dump['areas'][k] = serializeArea(v)
		
	dump['player'] = serializePlayer(world.player)
	
	return json.dumps(dump, sort_keys=True)
	
		
def serializeArea(area):

	dump = {}
	if area == None:
		return dump
		
	dump['name'] = area.name
	dump['entranceText'] = area.entranceText
	
	dump['features'] = []
	for feature in area.features:
		dump['features'].append( serializeFeature(feature) )
	
	return dump

	
def serializeFeature(feature):
	
	dump = {}
	if feature == None:
		return dump
		
	dump['name'] = feature.name
	dump['description'] = feature.description
	
	dump['actions'] = []
	for action in feature.actions:
		dump['actions'].append( serializeAction( action ) )

	return dump
	
	
def serializeAction(action):

	dump = {}
	if action == None:
		return dump

	dump['type'] = action.type
	dump['description'] = action.description
	dump['actionText'] = action.actionText

	if isinstance(action, common.PlayerMoveAction):
		dump['destination'] = action.destination.id

	return dump


def serializePlayer(player):

	dump = {}
	if player == None:
		return dump

	dump['name'] = player.name
	dump['currentArea'] = player.currentArea.id
	dump['inventory'] = []
	for i in player.inventory:
		dump['items'].append(i)

	return dump
	
