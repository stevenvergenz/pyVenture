from features import Room

########################
# The game loop
########################

def main():
	spawn = buildWorld()
	currentLocation = spawn
	
	while True:
	
		
		print currentLocation.entranceDescription
			
		passages = []
		choice = -1
		currentLocation.printPassages()
		print 'Where do you want to go?'
		try:
			choice = int(raw_input('> '))
		except ValueError:
			print 'Invalid choice, exiting'
			break
		except:
			continue
		
		if choice <= len(currentLocation.passages) and choice > 0:
			currentLocation = currentLocation.getRoom(choice)
		else:
			print 'That is not an option.'
			
		print
		print


def buildWorld():

	#####################################
	# Build the (rather limited) world
	#####################################
	spawn = Room('Birth Springs', 
		entranceDescription = 'You awake in a dark, warm, and wet stone room.')
	courtyard = spawn.addAdjacentRoom(
		Room('Courtyard', 'You arrive in a decent-sized dirt yard, open to the sky, with some practice dummies set up.'),
		passageDescription = 'A dark tunnel with a bright light at the end')
	
	courtyard.addAdjacentRoom(
		Room('Library', 'You arrive in a well-lit room with shelves and shelves of musty-smelling books.'),
		passageDescription = 'A stairway up to a tower to the west, leading to an impressive-looking set of double doors',
		returnDescription = 'Large oak double doors to the east')
	
	courtyard.addAdjacentRoom(
		Room('Armory', 'You arrive in an iron-smelling room full of racks of weapons and armor.'),
		passageDescription = 'A door to the south set into the wall of a stone tower',
		returnDescription = 'A wooden door on the north side of the room')
	
	courtyard.addAdjacentRoom(
		Room('Great Hall', 'You arrive in a long firelit room with two long tables running down its center and a raised platform at the end.'),
		passageDescription = 'A few stairs to the east leading up to a large pair of ornately-carved doors',
		returnDescription = 'Large double doors on the west side of the hall')
	
	return spawn	
