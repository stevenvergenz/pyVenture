from common import Area, Passage, Action, Player

def main():

	spawn = Area('birth springs', 'you awake in a derpy place')
	
	courtyard = Area('courtyard', 'you arrive in a bright dirt yard')
	spawn.features.append( Passage('southward door', 'a dark tunnel', courtyard) )
	
	player = Player('Steven')
	player.moveTo(spawn)
	
	while(True):
	
		for feature in player.currentArea.features:
			print feature.description
			
		print 'What do you want to do?'
		
		actionlist = []
		for feature in player.currentArea.features:
			for action in feature.actions:
				print '{0}. {1}'.format(len(actionlist), action.description)
				actionlist.append(action)
				
		choice = int(raw_input('> '))
		actionlist[choice].execute(player)
