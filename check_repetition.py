### CSCE 121 Mimir Grading Supplements
### Author: Seth Polsley, 11/5/18
### Purpose: Evaluates amount of repetition across input files
### Used for Abstraction rubric item, 2 pts. total (repeating code is probably top indicator of poor abstraction; other related issues could fall under Flow or Additional Considerations)

import os, sys
from difflib import SequenceMatcher

# A simple approach to detecting repetition in code
# 1. Read all lines, counting duplicates, and sorting the remainder
# 2. Use difflib to compare similarity of remaining and count those above a certain threshold
# 3. Print results

# GLOBALS
# Weights of each type of error
WEIGHT_DUP = 0.8 # exact duplicate lines weighting
WEIGHT_SIM = 0.65 # similar lines weighting

# Thresholds for similarity and line length
SIM_THRESH = 0.9 # similarity threshold
LEN_THRESH = 22 # line character length threshold in order to be considered as candidate


# Functions
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def parse_line(x):
	return x.split('//')[0].strip() # remove comments and whitespace

# usage checks
if len(sys.argv) < 2:
	print("No CPP files provided!")
	print("0")
	exit()

# Step 1: Read all files into the collection of lines
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
				source_lines.append(source_line)

# count duplicates, and sort
content = [parse_line(x) for x in source_lines if x.strip() != '' and len(parse_line(x)) > LEN_THRESH] # remove whitespace and comments for checking and sorting, no blank lines
lines = len(content) # count original, non-new lines

uniques = set(content)
remainder = list(uniques) # get only uniques
duplicates = lines - len(remainder) # count duplicates

remainder.sort() # sort list of remainder


# Step 2: Using difflib, determine how many in the remainder are similar above a threshold
similar = 0
i = 0
j = 0
while i < len(remainder) and j < len(remainder)-1:
	j += 1 # increment j at start
	if similarity(remainder[i],remainder[j]) > SIM_THRESH and len(remainder[i]) > 30: # 90% similar for long-ish lines of code
		similar += 1
		i -= 1 # keep i at start of group while j steps through to find end to similarities
	else:
		i = j - 1 # move i forward to end of current similarity group
	i += 1 # increment i at end


# Step 3: Print final report
print("Total Candidate Lines (length threshold of " + str(LEN_THRESH) + "): " + str(lines))
print("Lines Fully Duplicated: " + str(duplicates))
print("Lines Over Similarity Threshold of " + str(SIM_THRESH*100) + "%: " + str(similar))

ratio = 100 * (WEIGHT_DUP*duplicates + WEIGHT_SIM*similar) / float(lines) # Final ratio

if ratio < 20:
	feedback = "There is very little repetition in your code"
	score = 100
elif ratio < 40:
	feedback = "There is some repetition in your code; consider simplifying logic or moving some common operations into their own functions"
	score = 75
elif ratio < 65:
	feedback = "There is a fair amount of repetition in your code; simplify logic or move common operations into their own functions"
	score = 50
else:
	feedback = "There is a lot of repetition in your code; simplify logic or move common operations into their own functions"
	score = 25

print("")
print("Reptition Rate: {0:.2f}%".format(ratio))
print("Feedback: " + feedback)
print(score)
