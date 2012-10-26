class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.description = description
		self.actions = {}
		
		# add 'describe' action
		def describe():
			print self.description
		self.actions['describe'] = describe

		
class Room:

	# Static members and functions
	List = []
	__idCounter = 0
	
	@staticmethod
	def getID():
		Room.__idCounter += 1
		return Room.__idCounter-1
	
	
	# Instance members
	def __init__(self, name, entranceDescription = ''):
	
		self.entranceDescription = entranceDescription
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