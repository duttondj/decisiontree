# Danny Dutton
# ECE4544

import decisiontree
import sys
from cStringIO import StringIO

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

# Should be switched but I messed up the file names
tdf = "training_data/rt"
idf = "input_data/ri"
cannot_compute = []

print("Num of Training Data Examples  | Number of Input Data Queries | Error Rate of Predictions")
print("-------------------------------|------------------------------|--------------------------")


for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
	decisiontree.train("RestaurantAttributes.txt", tdf+str(i)+".csv", "RestOut.txt")
	with Capturing() as output:
		try:
			decisiontree.predict("RestaurantAttributes.txt", idf+str(12-i)+".csv", "RestOut.txt")
		except IndexError:
			cannot_compute = i

	error_num = 0
	total_num = 0

	for line in output:
		line = line[-11:]

		line = line.translate(None, "\']:")

		line = ''.join(line).strip()
		line = line.split()

		if line[0] != line[1]:
			error_num += 1
		total_num += 1

	print error_num
	print total_num

	if cannot_compute != i:
		print(str(i)+"\t\t\t       | " + str(12-i) +"\t\t\t      | " + str(float(error_num)/float(total_num) * 100) + "%")
	elif cannot_compute == i:
		print(str(i)+"\t\t\t       | " + str(12-i) +"\t\t\t      | Error: Decision tree missing attributes")