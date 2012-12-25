import sys

def main():
	try:
		if sys.argv[1] == 'play':
			import launchGame

		elif sys.argv[1] == 'mapbuilder':
			import launchMapbuilder
		else:
			print sys.argv[1]
	except IndexError:
		print "Please use either 'play' or 'mapbuilder' as arguments to begin."

if __name__ == '__main__':
	main()
