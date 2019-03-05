### CSCE 121 Mimir Grading Supplements
### Author: Seth Polsley, 11/15/18
### Purpose: Simple evaluation if some variable names have meaningful length and are scoped within loops
### Used for Variables rubric item, 2 pts. total (Just looking for short variable names is simple evaluator, along with loop scoping; other issues can fall under Additional Considerations)

import os, sys
from difflib import SequenceMatcher

# To evaluate variables, just look at some data type names and scoping of for loops; let other issues go into Additional Considerations
# 1. Read all lines
# 2. Count short name variables and scoping in loops
# 3. Print results

# GLOBALS
# Weights of each type of error
WEIGHT_SHORT = 1 # short var names
WEIGHT_SCOPE = 0.5 # for loop counters not tightly scoped

# Thresholds
THRESH_SHORT = 3 # minimum number of permitted characters before considered short


# usage checks
if len(sys.argv) < 2:
	print("No CPP files provided!")
	print("0")
	exit()

# Step 1: Read all files into the collection of lines, ignoring comments and blocks of comments
source_lines = []
for f in range(1,len(sys.argv)):
	if not os.path.exists(sys.argv[f]):
		print("File '" + sys.argv[f] + "' not found!")
		print("0")
		exit()
	with open(sys.argv[f]) as source:
		code_block = False
		for source_line in source:
			if '/*' in source_line:
				code_block = True
			if '*/' in source_line:
				code_block = False
			if not code_block:
				source_lines.append(source_line.split('//')[0].strip()) # if not in code block, insert line with comments removed

# Step 2: Count short variable names and look at loop scoping
var_names = 0
var_names_short = 0
for_loops = 0
for_loops_scoped = 0
for line in source_lines:
	# Check variable naming
	temp = line.split(' ')
	if len(temp) > 1:
		if temp[0] == 'int' or temp[0] == 'double' or temp[0] == 'float' or temp[0] == 'bool' or temp[0] == 'char' or temp[0] == 'string':
			var_names += 1
			if len(temp[1]) < THRESH_SHORT:
				var_names_short += 1
	# Check scoping on loops
	if 'for' in line:
		for_loops += 1
		if 'int' in line or 'auto' in line or 'decltype' in line:
			for_loops_scoped += 1

# Step 3: Print final report
print("Total Short Variable Names: " + str(var_names_short) + " out of " + str(var_names) + " considered")
print("Total Scoping Issues: " + str(for_loops - for_loops_scoped) + " out of " + str(for_loops) + " considered")

ratio = 100 * (.5*(WEIGHT_SCOPE*(for_loops-for_loops_scoped))/float(for_loops) + .5*(WEIGHT_SHORT*var_names_short)/float(var_names))

if ratio < 15:
	feedback = "A few variable names may be short and minor scoping issues my be present but not enough to cause concern"
	score = 100
elif ratio < 30:
	feedback = "Several variable naming or scoping issues are present; remember to use meaningful names and scope variables tightly"
	score = 75
elif ratio < 50:
	feedback = "Multiple variable naming or scoping issues are present; make sure to use meaningful names and scope variables tightly"
	score = 50
else:
	feedback = "Many variable naming or scoping issues are present; you should use meaningful names and scope variables tightly"
	score = 25

print("")
print("Variable Naming or Scoping Issue Level: {0:.2f}%".format(ratio))
print("Feedback: " + feedback)
print(score)
