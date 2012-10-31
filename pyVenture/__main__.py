import sys

def main():

	if sys.argv[1] == 'play':
		import launchGame

	elif sys.argv[1] == 'mapbuilder':
		import launchMapbuilder
	else:
		print sys.argv[1]

if __name__ == '__main__':
	main()
