class Feature:

	def __init__(self, name, description):
	
		self.name = name
		self.actions = {}
		
		# add 'describe' action
		def describe():
			print description
		self.actions['describe'] = describe
	