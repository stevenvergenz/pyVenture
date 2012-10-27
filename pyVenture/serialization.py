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
	dump['entranceDescription'] = area.entranceDescription
	
	dump['features'] = []
	for feature in area.features:
		dump['features'].append( serializeFeature(feature) )
	
	
def serializeFeature(feature):
	
	dump = {}
	if feature == None:
		return dump
		
	dump['name'] = feature.name
	dump['description'] = feature.description
	
	if isinstance(feature, Passage):
		dump['type'] = 'passage'
		dump['destination'] = feature.destination.id
	
	dump['actions'] = {}
	for action in feature.actions:
		
	
	
def serializePlayer(player):

	pass
	