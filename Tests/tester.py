import subprocess

PYTHON = "dp_jjtl24.py"
TESTSEQUENCES = "../TestSequences/"

lengths = [3,4,5,6,7,8,9,10,11,15,20,50,100,200,500,1000,2000,3000,4000,5000,10000]
labels = ['A', 'B']

f = open("tests.txt", "w+")
f.write("")
f.close()

f=open("tests.txt", "a+")
for i in range(0, len(lengths)):
	for l in range(0, len(labels)):

		for j in range(i, len(lengths)):
			for m in range(l,len(labels)):
				file1 = "length" + str(lengths[i]) + "_" + labels[l] + ".txt"
				file2 = "length" + str(lengths[j]) + "_" + labels[m] + ".txt"

				output = subprocess.Popen("python " + PYTHON + " " + TESTSEQUENCES + file1 + " " + TESTSEQUENCES + file2 + "", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				out, err = output.communicate()

				print(file1, file2, out.split("\n")[1][12:][:-3])

				
				f.write(file1 + ",	" + file2 + ", " + out.split("\n")[1][12:][:-3] + "\n")

f.close()