import sys

mainMenu = {"player": {"currentArea": "Ring of Stones 1", "inventory": [], "name": "Hero"}, "areas": [{"entranceText": "You become aware in the center of a ring of standing stones amid a heavy fog. The air crackles with energy.", "features": [{"name": "familiar dolmen", "actions": [{"description": "Pass through the familiar dolmen", "events": [{"text": "You pass through the familiar dolmen.", "type": "TextEvent"}, {"destination": "Load game 1", "type": "PlayerMoveEvent"}]}, {"description": "Examine the familiar dolmen", "events": [{"text": "Though you do not recognize the stone portal, there is something strangely familiar about it.", "type": "TextEvent"}]}], "description": "A strangely familiar dolmen to your left with the inscription: \"THAT WHICH WAS\""}, {"name": "unfamiliar dolmen", "actions": [{"description": "Pass through the unfamiliar dolmen", "events": [{"text": "You pass through the unfamiliar dolmen.", "type": "TextEvent"}, {"destination": "New game 1", "type": "PlayerMoveEvent"}]}, {"description": "Examine the unfamiliar dolmen", "events": [{"text": "The stone portal seems to exude an air of newness and excitement.", "type": "TextEvent"}]}], "description": "An unfamiliar dolmen to the right with the inscription: \"THAT WHICH WILL BE\""}, {"name": "orb", "actions": [{"description": "Examine the orb", "events": [{"text": "The orb is rather innocuous, but you can sense the very powers of creation in its depths.", "type": "TextEvent"}]}, {"description": "Touch the orb", "events": [{"text": "The Mapbuilder launches!", "type": "TextEvent"}]}], "description": "A cloudy orb hovering in the center of the room"}], "name": "Ring of Stones", "id": "Ring of Stones 1"}, {"entranceText": "You see before you a sea of infinite potentiality. Some potentials seem within grasp.", "features": [{"name": "return path", "actions": [{"description": "Go back through the dolmen", "events": [{"text": "You go back through the dolmen.", "type": "TextEvent"}, {"destination": "Ring of Stones 1", "type": "PlayerMoveEvent"}]}], "description": "The dolmen returning you to the ring of stones."}], "name": "New game", "id": "New game 1"}, {"entranceText": "You see before you a myriad of shadowy individuals. Some seem close enough to touch.", "features": [{"name": "return path", "actions": [{"description": "Go back through the dolmen", "events": [{"text": "You go back through the dolmen to the ring of stones.", "type": "TextEvent"}, {"destination": "Ring of Stones 1", "type": "PlayerMoveEvent"}]}], "description": "The dolmen leading you back to the ring of stones"}], "name": "Load game", "id": "Load game 1"}]}



def main():

	if sys.argv[1] == 'play':
		import launchGame

	elif sys.argv[1] == 'mapbuilder':
		import launchMapbuilder
	else:
		print sys.argv[1]

if __name__ == '__main__':
	main()
