""" 
Danny Dutton

Using the DecisionTreeLearner from learning.py, this program will
produce a decision tree based on training data and attributes and 
writes it to a file. Additionally, it can predict class levels of 
input data by traversing the previously generated decision tree.
This program can also handle input/training data that uses N/A as
a value for an attribute. It will add additional lines of data to
cover all possible values of the attribute with the value of N/A.
Meaning, an attribute containing either Yes/No values will convert
a line containing N/A to two lines with a Yes and a No in place of
the N/A.

An example of the error rate of predict() is shown below using the
restaurant training data from the book. This is found using the 
Cross Validation method, however my method of Cross Validation is
not able to compute an answer if the decision tree is missing an 
attribute due to the decision tree being computed using training 
data that is missing the attribute in the first place. From my 
testing, a meaningful answer is not obtained until there are at 
least 5 training data examples. The value obtained from the first
instance where there is only one training data example is simply
due to a 50/50 chance of the sinlge leaf on the decision tree
matching the actual class level for the remaining queries. There
would probably be better error rates if I had more training data
to use in cross validation. The code I used to compute cross
validation can be found in crossvalidation.py. The data I used 
can be found in training_data/ and input_data/. The restaurant
attributes given in the spec sheet should be used.

Num of Training Data Examples  | Num of Input Data Queries | Error Rate of Predictions
-------------------------------|---------------------------|--------------------------
1                              | 11                        | 54.5454545455%
2                              | 10                        | Error: Decision tree missing attributes
3                              | 9                         | Error: Decision tree missing attributes
4                              | 8                         | Error: Decision tree missing attributes
5                              | 7                         | 57.1428571429%
6                              | 6                         | 66.6666666667%
7                              | 5                         | 40.0%
8                              | 4                         | 50.0%
9                              | 3                         | 66.6666666667%
10                             | 2                         | 50.0%
11                             | 1                         | 100.0%

"""

import learning
import random
import csv
import sys
from copy import deepcopy
from cStringIO import StringIO
import sys

""" Used to capture stdout from functions """
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

""" Import a CSV file and return a list of lists """
def import_csv(csvfile):
	f = open(csvfile, 'rb')

	lines = []
	line = []

	try:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row:
				for e in row:
					line.append(e.strip())
				lines.append(line)
				line = []
	except:
		print("ERROR: Could not open file: " + csvfile)
	finally:
		f.close()

	return lines

""" Take in training attributes and training data to compute 
a decision tree and store it as a file. Uses the 
DecisionTreeLearner function in learning.py from aima-python """
def train(ta_file, td_file, dt_file):
	training_attr = import_csv(ta_file)
	training_data = import_csv(td_file)

	attr_names = []

	# Get attribute names
	for line in training_attr:
		attr_names.append(line[0])

	# Check for any N/A in the data file
	for i, line in enumerate(training_data):
		if "N/A" in line:
			for j, x, in enumerate(line):
				if x == "N/A":
					na_index = j

			attr_match = training_attr[na_index]

			# Get the number of possible outcomes for an attribute
			attr_match_num = len(attr_match)

			# Append new lines containing actual data for N/A
			for k in range(1, attr_match_num):
				new_line = deepcopy(training_data[i])
				new_line[na_index] = attr_match[k]
				training_data.append(new_line)
				new_line = []

			training_data.remove(line)
	
	attr_names_str = " ".join(map(str, attr_names))
	
	random.seed()

	dataset = learning.DataSet(examples=training_data, attrnames=attr_names_str)
	decision_tree = learning.DecisionTreeLearner(dataset)
	with Capturing() as output:
		decision_tree.display()

	fo = open(dt_file, "w+")
	try:
		for line in output:
			fo.write(line + "\n")
	except:
		print("ERROR: Could not write to: " + dt_file)
	finally:
		fo.close()

""" Using decision tree from file and training attributes, predict
the class level of a set of input data values and print out the
input data along with the predicted class level. The class level
is predicted by using the input data to follow the decision tree
until an answer is found. """
def predict(ta_file, id_file, dt_file):
	training_attr = import_csv(ta_file)
	input_data = import_csv(id_file)

	with open(dt_file, "rb") as f:
		dt = f.readlines()

	attr_names = []

	# Get attribute names
	for line in training_attr:
		attr_names.append(line[0])

	# Check for any N/A in the data file
	for i, line in enumerate(input_data):
		if "N/A" in line:
			for j, x, in enumerate(line):
				if x == "N/A":
					na_index = j

			attr_match = training_attr[na_index]

			# Get the number of possible outcomes for an attribute
			attr_match_num = len(attr_match)

			# Append new lines containing actual data for N/A
			for k in range(1, attr_match_num):
				new_line = deepcopy(input_data[i])
				new_line[na_index] = attr_match[k]
				input_data.append(new_line)
				new_line = []

			input_data.remove(line)

	results = []

	

	for i, example in enumerate(input_data):
		# Get the first attribute since that is
		# what is next
		if len(dt) > 1:
			next_attr = dt[1].split(" ")[0]

		# Go through each branch of the decision tree
		for j, line in enumerate(dt):
			# Remove lead/trailing whitespace and split the line
			line = line.strip()
			branch = line.split(" ")

			# If on the first line, check if there is a single leaf 
			# in the tree. If not, go to the next line as the first line
			# isn't important
			if (j == 0) and (branch[0] == "RESULT"):
				results.append(branch[-1])
				break
			elif j == 0:
				continue

			# Check if current branch is on the same level
			# as where we need to be or if we are free to move
			# to the next level
			if (next_attr == branch[0]) or (next_attr == ""):
				# Branch contains attr and matching value
				if branch[2] == example[attr_names.index(branch[0])]:
					next_attr = ""

					# Branch goes to a leaf
					# Also set next attr as one that won't occur
					if branch[-3] == "RESULT":
						results.append(branch[-1])
						break;
				# Branch is not what we are looking for so go to the next
				# branch of identical attribute
				else:
					next_attr = branch[0]

	# Print out predictions
	for i, vector in enumerate(input_data):
		print(str(input_data[i]) + " : " + str(results[i]))


def cross_validation(ta_file, td_file, k=10, trials=1):
	training_attr = import_csv(ta_file)
	training_data = import_csv(td_file)

	attr_names = []

	# Get attribute names
	for line in training_attr:
		attr_names.append(line[0])

	# Check for any N/A in the data file
	for i, line in enumerate(training_data):
		if "N/A" in line:
			for j, x, in enumerate(line):
				if x == "N/A":
					na_index = j

			attr_match = training_attr[na_index]

			# Get the number of possible outcomes for an attribute
			attr_match_num = len(attr_match)

			# Append new lines containing actual data for N/A
			for k in range(1, attr_match_num):
				new_line = deepcopy(training_data[i])
				new_line[na_index] = attr_match[k]
				training_data.append(new_line)
				new_line = []

			training_data.remove(line)
	
	attr_names_str = " ".join(map(str, attr_names))
	
	random.seed()

	dataset = learning.DataSet(examples=training_data, attrnames=attr_names_str)

	return learning.cross_validation(learning.DecisionTreeLearner, dataset, k, trials)


if __name__ == "__main__":
	train("attributes/RestaurantAttributes.txt", "training_data/Restaurant.csv", "RestOut.txt")
	print("Input data and predictions:")
	predict("attributes/RestaurantAttributes.txt", "input_data/Restaurant.csv", "RestOut.txt")
	print
	print("Cross Validation (1 trial):    " + str(cross_validation("attributes/RestaurantAttributes.txt", "training_data/Restaurant.csv", 10, 1)))
	print("Cross Validation (10 trials):  " + str(cross_validation("attributes/RestaurantAttributes.txt", "training_data/Restaurant.csv", 10, 10)))
	print("Cross Validation (100 trials): " + str(cross_validation("attributes/RestaurantAttributes.txt", "training_data/Restaurant.csv", 10, 100)))
