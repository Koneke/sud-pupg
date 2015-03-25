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
		self.aliases = {}
		self.aliases["w"] = "west"
		self.aliases["e"] = "east"
		self.aliases["n"] = "north"
		self.aliases["s"] = "south"
		self.aliases["l"] = "look"

		self.playerLocation = None

	def parseCommand(self, command):
		command = command.strip()
		command = re.sub(" +", " ", command)
		
		arg = None
		if " " in command: #if we have an argument...
			head, arg = command.split(" ", 1)
		else:
			head = command

		if head in self.aliases:
			head = self.aliases[head]

		return head, arg

	def execCommand(self, command, arg = None):
		#print("execing:",command, arg)
		if command in self.playerLocation.exits:
			print("Going to:", self.playerLocation.exits[command])

def main():
	scr = scripty.loadScript('sud_scr.sc')
	#scripty.printBlock(scr)
	#for b in scr.getBlock("room"):
		#print(b.getKvp("name").value)

	rooms = [Room(b) for b in scr.getBlock("room")]
	rd = {}
	for room in rooms:
		"""print(room.name)
		print(room.ident)
		print(room.description)
		print(room.exits)
		print()"""
		rd[room.ident] = room
	#print(rd)

	gameinfo = scr.getBlock("gameinfo")

	g = Game()
	g.playerLocation = rd[gameinfo.getKvp("start").value]
	#print(g.playerLocation)

	#print(g.parseCommand("   w  bar baz"))
	g.execCommand(*g.parseCommand("w"))

main()
