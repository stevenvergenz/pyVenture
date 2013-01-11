
class GameStatus:
	Error = -1
	Quit = 0
	LaunchMapbuilder = 1
	LoadMap = 2
	


def main(world):

	player = world.player

	while(True):

		print
		print
		print player.currentArea.entranceText
		print
		print 'The area contains:'
		for feature in player.currentArea.features:
			print feature.description
			
		print 'What do you want to do?'
		
		actionlist = []
		for feature in player.currentArea.features:
			for action in feature.actions:
				print '{0}. {1}'.format(len(actionlist)+1, action.description)
				actionlist.append(action)
				
		try:
			choice = ''
			while choice == '':
				choice = raw_input('> ')
		except (KeyboardInterrupt, EOFError):
			return GameStatus.Quit

		print
		
		if choice.lower() in ['quit', 'q']:
			return GameStatus.Quit
		else:
			status = actionlist[int(choice)-1].trigger(player)
			if status is not None:
				return status


if __name__ == '__main__':
	main()
