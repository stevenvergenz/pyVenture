import common

def main():

	spawn = common.Area('birth springs', 'you awake in a derpy place')
	
	courtyard = common.Area('courtyard', 'you arrive in a bright dirt yard')
	spawn.features.append( common.Passage('southward door', 'a dark tunnel', courtyard) )
	
	player = common.Player('Steven')
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
				
		choice = raw_input('> ')
		print
		
		if choice == 'quit':
			break
		else:
			actionlist[int(choice)].execute(player)
