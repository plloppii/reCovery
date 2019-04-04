line = "G0 F4500 X58.077 Y47.698 Z0.500"
line1 = "G1 Z2.260 F1002"


i = line.find("Z")
l = len(line)-1
z=""
while(i+1<=l and line[i+1] != " "):
	z += line[i+1]
	i+=1

print(z)
'''
z = "0"
i = 0
extracted= False
for char in line:
	if char == "Z":
		while(not extracted):
			try:
				while(line[i+1]!=" "):
					print(line[i+1])
					z += line[i+1]
					i+=1
				extracted = True
			except IndexError:
				break
	i+=1
print(z)
'''