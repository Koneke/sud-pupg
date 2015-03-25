#just a convenience for the scriptfile reading
#not using just a 'count' since we might, theoretically, want tabs in the data.
def getTabs(string):
	for i in range(len(string)):
		if string[i] != '\t':
			return i
	return 0

#not really needed repetitionwise (DRY), but makes for more readable code overall.
def dedent(string, amt):
	if getTabs(string) < amt:
		raise Exception("Tried to dedent further than there was tabs.")
	return string[amt:]

class kvp(object):
	def __init__(self, k = None, v = None):
		self.key = k
		self.value = v

	def __str__(self):
		return self.key + ", " + self.value

class block(object):
	def __init__(self):
		#kvps is not a dict, since we allow multiple keys with same value
		#(they are not really true keys, but we use the structure for
		#function calls and such).
		self.name = ""
		self.kvps = []
		self.blocks = []

	#note, case sensitive
	def getKvp(self, name):
		kvps = [kvp for kvp in self.kvps if kvp.key == name]

		if len(kvps) < 1:
			#raise Exception("No such key.")
			return None
		if len(kvps) < 2:
			return kvps[0]
		return kvps

	def getBlock(self, name):
		blocks = [b for b in self.blocks if b.name == name]

		if len(blocks) < 1:
			#raise Exception("No such key.")
			return None
		if len(blocks) < 2:
			return blocks[0]
		return blocks

def readBlock(name, lines):
	currentBlock = block();
	currentBlock.name = name
	lines = [dedent(l, getTabs(lines[0])) for l in lines]
	i = 0
	while i < len(lines):
		if ':' in lines[i]: #kvp
			key = lines[i].split(':')[0]
			value = lines[i][1+len(key):]
			#currentBlock.kvps.append((key, value))
			currentBlock.kvps.append(kvp(key, value))
			i += 1
		else: #block, make sure not to use colons in the data
			j = i
			while True:
				j += 1
				#don't read unindented stuff, or past the EOF
				if j == len(lines): break
				if getTabs(lines[j]) <= getTabs(lines[i]): break
			currentBlock.blocks.append(readBlock(lines[i], lines[i+1:j]))
			#skip the block, since it's already handled by the recursive call.
			i = j
	return currentBlock

def printBlock(block, indent=0):
	indentation = "    "
	print(indentation * indent, '[', block.name, ']', sep="")

	if(len(block.kvps) > 0):
		print(indentation * (indent + 1), "Keys:", sep="")
		for kvp in block.kvps:
			print(indentation * (indent + 1), kvp, sep="")

	if(len(block.blocks) > 0):
		print(indentation * (indent + 1), "Blocks:", sep="")
		for b in block.blocks:
			printBlock(b, indent+1)

def loadScript(path):
	f = open(path)
	lines = [l.strip('\n') for l in f.readlines() if l.strip() != ""]
	return readBlock(lines[0], lines[1:])
