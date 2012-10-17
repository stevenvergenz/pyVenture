# pySOG.py
class Room:

	# Static members and functions
	List = []
	__idCounter = 0
	
	@staticmethod
	def getID():
		Room.__idCounter += 1
		return Room.__idCounter-1
	
	
	# Instance members
	def __init__(self, name, description = ''):
	
		self.description = description
		self.id = Room.getID()
		self.name = name
		self.passages = []
    
		Room.List.append(self)
		
    
	def addAdjacentRoom( self, adjacentRoom, passageDescription, returnDescription = None ):
	
		if isinstance(adjacentRoom, Room):
			room = adjacentRoom
		elif isinstance(room, string):
			room = Room(adjacentRoom)
		else:
			raise TypeError('Room representation must be a Room object or a string')

		self.passages.append( (room,passageDescription) )
		if returnDescription != None:
			room.addAdjacentRoom(self, returnDescription)
		return room
		
	# end function addAdjacentRoom
	
	
	def printPassages( self ):
	
		print 'From here, there {0} {1} passage{2} out:'.format(
			'is' if len(self.passages)==1 else 'are',
			len(self.passages), 
			's' if len(self.passages)!=1 else ''
			)
		
		itemnum = 1
		for room, desc in self.passages:
			print '{}. {}'.format(itemnum, desc)
			itemnum += 1
        
		
	def getRoom( self, passageNum ):
		return self.passages[passageNum-1][0]
		
# end class Room


#####################################
# Build the (rather limited) world
#####################################
spawn = Room('Birth Springs', 'a dark, warm, and wet stone room')
courtyard = spawn.addAdjacentRoom(
	Room('Courtyard', 'a decent-sized dirt yard, open to the sky, with some practice dummies set up'),
	passageDescription = 'A dark tunnel with a bright light at the end')

courtyard.addAdjacentRoom(
	Room('Library', 'a well-lit room with shelves and shelves of musty-smelling books'),
	passageDescription = 'An stairway up to a tower to the west, leading to an impressive-looking set of double doors',
	returnDescription = 'Large oak double doors to the east')

courtyard.addAdjacentRoom(
	Room('Armory', 'an iron-smelling room full of racks of weapons and armor'),
	passageDescription = 'A door to the south set into the wall of a stone tower',
	returnDescription = 'A wooden door on the north side of the room')

courtyard.addAdjacentRoom(
	Room('Great Hall', 'a long firelit room with two long tables running down its center and a raised platform at the end'),
	passageDescription = 'A few stairs to the east leading up to a large pair of ornately-carved doors',
	returnDescription = 'Large double doors on the west side of the hall')
	
	
########################
# The game loop
########################

currentLocation = spawn

while True:

	if( currentLocation == spawn ):
		print 'You awake in', currentLocation.description
	else:
		print 'You arrive in', currentLocation.description
		
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
		