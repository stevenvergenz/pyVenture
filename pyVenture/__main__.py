import sys, glob, json, gzip

from common import events, types
from game.main import main as launchGame, GameStatus
from mapbuilder.main import main as launchMapbuilder


#################################################
### Build the main menu based on available files
#################################################


def buildMenu():

	mainMenu = {"areas": [{"entranceText": "You become aware in the center of a ring of standing stones amid a heavy fog. The air crackles with energy.", "features": [{"name": "familiar dolmen", "actions": [{"description": "Pass through the familiar dolmen", "events": [{"text": "You pass through the familiar dolmen.", "type": "TextEvent"}, {"destination": "Load game 1", "type": "PlayerMoveEvent"}]}, {"description": "Examine the familiar dolmen", "events": [{"text": "Though you do not recognize the stone portal, there is something strangely familiar about it.", "type": "TextEvent"}]}], "description": "A strangely familiar dolmen to your left with the inscription: \"THAT WHICH WAS\""}, {"name": "unfamiliar dolmen", "actions": [{"description": "Pass through the unfamiliar dolmen", "events": [{"text": "You pass through the unfamiliar dolmen.", "type": "TextEvent"}, {"destination": "New game 1", "type": "PlayerMoveEvent"}]}, {"description": "Examine the unfamiliar dolmen", "events": [{"text": "The stone portal seems to exude an air of newness and excitement.", "type": "TextEvent"}]}], "description": "An unfamiliar dolmen to the right with the inscription: \"THAT WHICH WILL BE\""}, {"name": "orb", "actions": [{"description": "Examine the orb", "events": [{"text": "The orb is rather innocuous, but you can sense the very powers of creation in its depths.", "type": "TextEvent"}]}, {"description": "Touch the orb", "events": [{"text": "The power of creation fills you, you feel you could do anything!", "type": "TextEvent"}]}], "description": "A cloudy orb hovering in the center of the room"}], "name": "Ring of Stones", "id": "Ring of Stones 1"}, {"entranceText": "You see before you a sea of infinite potentiality. Some potentials seem within grasp.", "features": [{"name": "return path", "actions": [{"description": "Go back through the dolmen", "events": [{"text": "You go back through the dolmen.", "type": "TextEvent"}, {"destination": "Ring of Stones 1", "type": "PlayerMoveEvent"}]}], "description": "The dolmen returning you to the ring of stones."}], "name": "New game", "id": "New game 1"}, {"entranceText": "You see before you a myriad of shadowy individuals. Some seem close enough to touch.", "features": [{"name": "return path", "actions": [{"description": "Go back through the dolmen", "events": [{"text": "You go back through the dolmen to the ring of stones.", "type": "TextEvent"}, {"destination": "Ring of Stones 1", "type": "PlayerMoveEvent"}]}], "description": "The dolmen leading you back to the ring of stones"}], "name": "Load game", "id": "Load game 1"}], "player": {"currentArea": "Ring of Stones 1", "inventory": [], "name": "Hero"}}
	
	world = types.World.deserialize(mainMenu)
	
	# add the current directory's maps to the 'new game' room
	for name in glob.glob('*.pvm') + glob.glob('*.pvm.gz'):
		feature = types.Feature( name, 'A potential named {0}'.format(name) )
		feature.parentArea = world.areas[1]
		world.areas[1].features.append(feature)

		action = types.Action( 'Embody potential {0}'.format(name), 'A new universe spins off, and you are caught in the middle of it!' )
		action.parentFeature = feature
		feature.actions.append(action)

		event = LoadWorldEvent()
		event.properties['filename'] = name
		event.parentAction = action
		action.events.append( event )

	# add the mapbuilder launcher
	event = LoadMapbuilderEvent()
	event.parentAction = world.areas[0].features[2].actions[1]
	world.areas[0].features[2].actions[1].events.append(event)

	# add the saved games to the 'load game' room

	return world


world = None

def main():

	# load the main menu
	menu = buildMenu()
	status = launchGame(menu)

	while status not in [GameStatus.Quit, GameStatus.Error]:
		status = launchGame(world)

	try:
		raw_input('Press Enter to exit...')
	except EOFError:
		print

	#if sys.argv[1] == 'play':
	#	launchGame()

	#elif sys.argv[1] == 'mapbuilder':
	#	launchMapbuilder()
	#else:
	#	print sys.argv[1]



###############################################
### Command events
###############################################

class LoadWorldEvent(events.Event):

	def __init__(self, properties = None):
		if properties is None:
			events.Event.__init__(self, {'filename': ''})
		else:
			events.Event.__init__(self, properties)


	def __call__(self, actor, action):
		dump = {}
		filename = self.properties['filename']
		with gzip.open(filename, 'r') if filename[-2:] == 'gz' else open(filename, 'r') as file:
			try:
				tempstr = file.read()
				dump = json.loads(tempstr)
			except:
				print 'There was a problem loading', filename

		# populate tree
		global world
		world = types.World.deserialize(dump)
		return GameStatus.LoadMap


class LoadMapbuilderEvent(events.Event):

	def __init__(self, properties = None):
		if properties is None:
			events.Event.__init__(self, {})
		else:
			events.Event.__init__(self, properties)


	def __call__(self, actor, action):
		print 'Launching the Map Builder...'
		launchMapbuilder()
	

if __name__ == '__main__':
	main()
