### CSCE 121 Mimir Grading Supplements
### Author: Seth Polsley, 11/15/18
### Purpose: Simple evaluation of expression complexity by counting number of long or compound expressions
### Used for Expression rubric item, 2 pts. total (Number of long, compound expressions is a sensible indicator of expression complexity)

import os, sys
from difflib import SequenceMatcher

# To evaluate expression complexity, we'll just look at compound expressions and long expression lines; that's the quickest, easiest indicator
# 1. Read all lines
# 2. Count compound operators (&&, ||) and constructs (if, else if, else, for, while) for comparison, plus length
# 3. Print results

# GLOBALS
# Weights of each type of error
WEIGHT_LEN = 0.6 # weight of long expressions

# Thresholds for line length counted as complex expression
LEN_THRESH = 50 # line character length threshold in order to be considered as a long expression


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

# Step 2: Count operators and long expressions
compounds = 0
constructs = 0
long_lines = 0
for line in source_lines:
	# Count compound operations on the line
	compounds += line.count('&&')
	compounds += line.count('||')
	# Count if line is a for, while, if construct
	if 'else if' in line or 'else' in line or 'while' in line or 'for' in line:
		constructs += 1
		compounds += 1 # add 1 compound for the statement itself (e.g. if (this || that) should count both sides)
		# if line was a construct, check if it was a lengthy expression
		if len(line) > LEN_THRESH:
			long_lines += 1

# Step 3: Print final report
print("Total Conditional Constructs: " + str(constructs))
print("Total Compound Expressions: " + str(compounds))
print("Total Lengthy Constructs: " + str(long_lines))

constructs_to_compounds_ratio = constructs/float(compounds) # constructs per compound, ideally 1-to-1, but gets smaller as expression complexity goes up (e.g. 2 compound per "if" would be 0.5 and 3 about 0.3)
# could use compounds to constructs but can grow unbounded as compounds increases; constructs to compounds is always between 0 and 1, decreasing, so just 1 - ratio to get percentage penalty
long_lines_to_constructs_ratio = (WEIGHT_LEN*long_lines)/float(constructs) # number of constructs that are over length threshold, scaled by cost of long expressions

ratio = 100 * (.5*long_lines_to_constructs_ratio + .5*(1 - constructs_to_compounds_ratio)) # Final rating

if ratio < 15:
	feedback = "There may be some complex or long expressions, but likely not enough to impact readability or suggest a need for better code design"
	score = 100
elif ratio < 30:
	feedback = "There are some unnecessary complex or long expressions; readability may be impeded and there may be a need for better code design to reduce complexity"
	score = 75
elif ratio < 50:
	feedback = "There are many unnecessary complex or long expressions; readability is likely impaired and there is probably better code design to reduce complexity"
	score = 50
else:
	feedback = "There are too many unnecessary complex or long expressions; readability will be impaired and there should be better code design to reduce complexity"
	score = 25

print("")
print("Complex Expression Rate: {0:.2f}%".format(ratio))
print("Feedback: " + feedback)
print(score)
