import sys
from mapbuilder.main import main as mapmain
from game.main import main as gamemain

def main():

	if sys.argv[1] == 'play':
		gamemain()

	elif sys.argv[1] == 'mapbuilder':
		mapmain()
	else:
		print sys.argv[1]

if __name__ == '__main__':
	main()
