from common.types import World, Player, Area, Feature, Action
from common.events import PlayerMoveEvent, gameHelp
import json

def buildWorld():

	dump = json.loads('{"player": {"inventory": [], "name": "Hero", "currentArea": "Courtyard 1"}, "areas": {"Library 1": {"entranceText": "You arrive in a quiet musty-smelling room with rows and rows of bookshelves.", "name": "Library", "features": [{"name": "eastern door", "actions": [{"description": "Enter eastern door", "events": [{"text": "You traverse the passage.", "type": "TextEvent"}, {"destination": "Courtyard 1", "type": "PlayerMoveEvent"}]}], "description": "Wooden double-doors to the east"}]}, "Courtyard 1": {"entranceText": "You arrive in a brightly lit dirt practice yard with several dummies set up.", "name": "Courtyard", "features": [{"name": "western stairway", "actions": [{"description": "Enter western stairway", "events": [{"text": "You traverse the passage.", "type": "TextEvent"}, {"destination": "Library 1", "type": "PlayerMoveEvent"}]}], "description": "A winding staircase to the west leading to a stone tower"}, {"name": "southern door", "actions": [{"description": "Enter southern door", "events": [{"text": "You traverse thepassage.", "type": "TextEvent"}, {"destination": "Armory 1", "type": "PlayerMoveEvent"}]}], "description": "A sturdy-looking wooden door to the south"}]}, "Birth Springs 1": {"entranceText": "You awake in a damp dark stone room.", "name": "Birth Springs", "features": [{"name": "dark tunnel", "actions": [{"description": "Enter dark tunnel", "events": [{"text": "You traverse the passage.", "type": "TextEvent"}, {"destination": "Courtyard 1", "type": "PlayerMoveEvent"}]}], "description": "A long dark tunnel to the south with a light at the end"}]}, "Armory 1": {"entranceText": "You arrive in a cramped room full of weapon and armor racks.", "name": "Armory", "features": [{"name": "northern door", "actions": [{"description": "Enter northern door", "events": [{"text": "You traverse the passage.", "type": "TextEvent"}, {"destination": "Courtyard 1", "type": "PlayerMoveEvent"}]}], "description": "A sturdy wooden door to the north"}]}}}')
	world = World.deserialize(dump)
	return world


def main():
	'''
	I am going to clean up this entire main with some new DEFS and whatnot. It WILL get big so might as well start early
	'''
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
				
		choice = raw_input('> ').lower()
		print
		
		if choice == 'quit' or choice == 'q':
			break
		elif choice == 'help' or choice == 'h':
			gameHelp()
		else:
			try:
				actionlist[int(choice)-1].trigger(player)
			except ValueError:
				print "May be bad entry from mistyping. Try again"

	print "THIS DUMP BELOW IS FOR DEBUG:"
	print "============================="
	print json.dumps( world.serialize())
	print "============================="
	raw_input('Press Enter to quit...')


if __name__ == '__main__':
	main()
