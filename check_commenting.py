### CSCE 121 Mimir Grading Supplements
### Author: Seth Polsley, 11/4/18
### Purpose: Counts comment-to-code ratio across input files
### Used for Documentation/Commenting rubric item, 2 pts. total

import sys, os

# This will be a simple way to calculate the commment-to-code ratio:
# Read line-by-line, count up lines, and count up comments if "//" or block detected

# usage checks
if len(sys.argv) < 2:
	print("No CPP files provided!")
	print("0")
	exit()

# read all files into the collection of lines
source_lines = []
for f in range(1,len(sys.argv)):
	if not os.path.exists(sys.argv[f]):
		print("File '" + sys.argv[f] + "' not found!")
		print("0")
		exit()
	with open(sys.argv[f]) as source:
		source_lines.extend(source.readlines())

# setup
lines = 1
codes = 0
comments = 0
in_block = False

# read line-by-line
for line in source_lines:
	lines += 1

	# count block comments
	if '/*' in line:
		in_block = True # open block

	if '*/' in line:
		in_block = False
		comments += 1 # blocks count as one

	# count standard comments
	if '//' in line and not in_block:
		comments += 1 # can have comment, whether on code line or not, but not in block

	# count code lines
	if not in_block and line.strip().find('//') != 0 and not line.strip() == '':
		codes += 1 # count line as code if not in block code or starting with commment

# print final report
print("Total Lines: " + str(lines))
print("Code Lines: " + str(codes))
print("Comments: " + str(comments))

ratio = comments*100/codes

if ratio < 6:
	feedback = "There are very few to no comments present; you should comment your code more thoroughly"
	score = 25
elif ratio < 12:
	feedback = "There are a few comments, but you should comment your code more completely for full credit"
	score = 50
elif ratio < 18:
	feedback = "There are some comments, but you should comment your code more completely for full credit"
	score = 75
elif ratio < 50:
	feedback = "There are a reasonable number of comments"
	score = 100
else:
	feedback = "Best practice is around 30% comments, so this is a bit more heavily commented than necessary. Comments can start to impede readability at a certain level."
	score = 75

print("")
print("Comment-to-Code Ratio: " + str(ratio) + "%")
print("Feedback: " + feedback)
print(score)
