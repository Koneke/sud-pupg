import scripty, re

class Room:
	def __init__(self, b = None):
		self.name = ""
		self.ident = ""
		self.description = ""
		self.exits = {}
		self.items = []

		if b != None:
			self.populateFromScripty(b)

	def __str__(self):
		return self.ident + ", " + self.name

	def populateFromScripty(self, block):
		self.name = block.getKvp("name").value
		self.description = block.getKvp("desc").value
		self.ident = block.getKvp("id").value

		exits = block.getBlock("exits")
		if exits != None:
			for kvp in exits.kvps:
				self.exits[kvp.key] = kvp.value

class Game():
	def __init__(self):
		#alises, list of lists of commands that should be considered the same
		#e.g., "w" and "west", "x" and "examine", usw
		self.aliases = []
		self.aliases.append(["w", "west"])
		self.aliases.append(["e", "east"])
		self.aliases.append(["n", "north"])
		self.aliases.append(["s", "south"])

		self.playerLocation = None

def parseCommand(command):
	command = command.strip()
	command = re.sub(" +", " ", command)
	print("<", command, ">", sep="")
	return command

def main():
	scr = scripty.loadScript('sud_scr.sc')
	#scripty.printBlock(scr)
	#for b in scr.getBlock("room"):
		#print(b.getKvp("name").value)

	rooms = [Room(b) for b in scr.getBlock("room")]
	rd = {}
	for room in rooms:
		print(room.name)
		print(room.ident)
		print(room.description)
		print(room.exits)
		print()
		rd[room.ident] = room
	print(rd)

	gameinfo = scr.getBlock("gameinfo")

	g = Game()
	g.playerLocation = rd[gameinfo.getKvp("start").value]
	print(g.playerLocation)

	print(parseCommand("   foo  bar "))

main()
