f1 = open("tests.txt", "r")

f2 = open("tests1.txt", "r")

print("If nothing shows up after this, there were no errors")

for line in f1:
	if line != f2.readline():
		print(line)

