from common import types
from common import events
import json, gzip, glob

world = None
player = None

class LoadWorldEvent(events.Event):

	def __init__(self, properties = None):
		if properties is None:
			Event.__init__(self, {'filename': ''})
		else:
			Event.__init__(self, properties)


	def __call__(self, actor, action):
		dump = {}
		with gzip.open(filename, 'r') if filename[-2:] == 'gz' else open(filename, 'r') as file:
			try:
				tempstr = file.read()
				dump = json.loads(tempstr)
			except:
				print 'There was a problem loading', filename

		# populate tree
		world = types.World.deserialize(dump)
		player = world.player


def buildWorld():

	pass


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


	print json.dumps( world.serialize() )
	raw_input('Press Enter to quit...')



if __name__ == '__main__':
	main()
