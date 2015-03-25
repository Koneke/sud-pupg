import scripty

class Room:
	def __init__(self):
		self.name = ""
		self.ident = ""
		self.description = ""
		self.exits = {}
		self.items = []

	def populateFromScripty(self, block):
		self.name = block.getKvp("name").value
		self.description = block.getKvp("desc").value
		self.ident = block.getKvp("id").value

		exits = block.getBlock("exits")
		print(exits)
		if exits != None:
			for kvp in exits.kvps:
				self.exits[kvp.key] = kvp.value

class game():
	def __init__(self):
		#alises, list of lists of commands that should be considered the same
		#e.g., "w" and "west", "x" and "examine", usw
		self.aliases = []
		self.aliases.append(["w", "west"])
		self.aliases.append(["e", "east"])
		self.aliases.append(["n", "north"])
		self.aliases.append(["s", "south"])

def main():
	scr = scripty.loadScript('sud_scr.sc')
	scripty.printBlock(scr)
	#for b in scr.getBlock("room"):
		#print(b.getKvp("name").value)

	r = Room()
	r.populateFromScripty(scr.getBlock("room")[0])
	print(r.name)
	print(r.ident)
	print(r.description)
	print(r.exits)

main()
