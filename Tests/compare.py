f1 = open("tests_ans2.txt", "r")

f2 = open("testsFF.txt", "r")

print("If nothing shows up after this, there were no errors")

for line in f1:
	if line != f2.readline():
		print(line)

