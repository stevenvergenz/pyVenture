from common import World, Player, Area, Feature, Action
from events import PlayerMoveEvent

import serialization

def buildWorld():

	rooms = [('Birth Springs', 'You awake in a damp dark stone room.'),
		('Courtyard', 'You arrive in a brightly lit dirt practice yard with several dummies set up.'),
		('Library', 'You arrive in a quiet musty-smelling room with rows and rows of bookshelves.'),
		('Armory', 'You arrive in a cramped room full of weapon and armor racks.')]

	passages = {'Birth Springs 1': [('dark tunnel', 'A long dark tunnel to the south with a light at the end', 'Courtyard 1')],
		'Courtyard 1': [('western stairway', 'A winding staircase to the west leading to a stone tower', 'Library 1'),
			('southern door', 'A sturdy-looking wooden door to the south', 'Armory 1')],
		'Library 1': [('eastern door', 'Wooden double-doors to the east', 'Courtyard 1')],
		'Armory 1': [('northern door', 'A sturdy wooden door to the north', 'Courtyard 1')]}

	world = World()
	world.player = Player('Hero')

	# initialize rooms
	for name, entranceText in rooms:
		room = Area(name, entranceText)
		world.addArea(room)


	# initialize passages
	for id, connections in passages.items():
		for passage in connections:
			feature = Feature(passage[0], passage[1])
			feature.parentArea = world.areas[passage[2]]
			action = Action('Enter '+passage[0], 'You traverse the passage.')
			action.events.append( PlayerMoveEvent( world.areas[passage[2]] ) )
			action.parentFeature = feature
			feature.actions.append(action)
			world.areas[id].features.append(feature)
	
	world.player.currentArea = world.areas['Birth Springs 1']
	return world


def main():

	world = buildWorld()
	player = world.player

	while(True):
	
		print player.currentArea.entranceText
		print 'The area contains:'
		for feature in player.currentArea.features:
			print feature.description
			
		print 'What do you want to do?'
		
		actionlist = []
		for feature in player.currentArea.features:
			for action in feature.actions:
				print '{0}. {1}'.format(len(actionlist)+1, action.description)
				actionlist.append(action)
				
		choice = raw_input('> ')
		print
		
		if choice == 'quit':
			break
		else:
			actionlist[int(choice)-1].trigger(player)


	print serialization.serializeWorld(world)

