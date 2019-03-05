### CSCE 121 Mimir Grading Supplements
### Author: Seth Polsley, 11/4/18
### Purpose: Reads through input files to evaluate indentation/formatting consistency
### Used for Indentation/Formatting rubric item, 2 pts. total

import sys, os, math

# This will be a very simplistic, somewhat kludgy, method for detecting indentation levels:
# 1. Read through line-by-line and save all indentation levels it sees
# 2. Pick the most likely indentation for a given level based on most frequent appearance
# 3. Read thorugh line-by-line again and mark unexpected if it doesn't match top pick

# GLOBALS
# Weights of each type of error
WEIGHT_WRONG = 1 # each line with fully wrong indentation has weight of 1
WEIGHT_PARTLY = 0.8 # each line of slightly wrong indentation only has weight of 0.8
WEIGHT_TABSPACE = 0.4 # each line of mixed tab space only has weight of 0.3

# Attempt to lessen impact of large blocks that are wrongly indented?
BLOCK_LEVEL = True # true makes lines be weighted slightly by blocks (lowers penalty for wrong level in one region, using function specified in BLOCK_ADJUST)
# Adjustment function for blocks, return new weight between 0 and 1; fewer blocks with more lines would be slightly less weight than many lines spread over many blocks
BLOCK_ADJUST = lambda lines,blocks: 1.0 if lines == 0 else math.log(blocks/float(lines))/math.log(1000) + 1 # This is a log base 1000 function that slowly reduces cost of block-level errors

# When calculating final result for many files, weight file by number lines or just average?
FILE_WEIGHT = True # files will be weighted by number of lines; turn to False to just take raw average


# Functions
def list_to_ranged_string(l):
	# build up string, combining consecutive line ranges
	result = ''
	prev_e = -1 # start is line -1, which will never happen since starts at 1
	in_range = False
	for e in l: # go through all line numbers in the list
		if e != prev_e + 1: # if not continuing in range
			if in_range: # must handle printing previous range
				result += "-" + str(prev_e)
				in_range = False
			if prev_e == -1:  # then print current line number, only with comma when not on first one (-1 for prev_e)
				result += str(e)
			else:
				result += ", " + str(e)
		else: # else, continuing a range
			in_range = True
		prev_e = e
	if in_range:
		result += "-" + str(prev_e) # must print last one if finished list in a range
	return result

# Usage checks
if len(sys.argv) < 2:
	print("No CPP files provided!")
	print("0")
	exit()

# Perform operations for all passed files
file_lines = []
file_ratios = []
for f in range(1,len(sys.argv)):
	if not os.path.exists(sys.argv[f]):
		print("File '" + sys.argv[f] + "' not found!")
		print("0")
		exit()

	# Step 1: First read-through to get all levels seen
	# setup
	indents = 0
	indents_probs = {}

	# read line-by-line
	with open(sys.argv[f]) as source:
		for line in source:
			# get line indentation
			indentation = line[:len(line)-len(line.lstrip())] # read from beginning until start of stripped string
			if '\n' not in indentation: # must have been a newline if \n present after stripping, ignore
				
				# check for decrease indentation, only if '}' at start
				if line.strip().find('}') == 0: # decrease
					indents -= 1

				# add to list tracking all seen indentations
				if indents not in indents_probs: # adding new level
					indents_probs[indents] = [indentation]
				else: # appending to existing level
					indents_probs[indents].append(indentation)

				# check for indentation changes, '{' always affects next line and '}' affects next line if with code this line
				if '{' in line: # increase
					indents += 1
				if '}' in line and not line.strip().find('}') == 0: # decrease
					indents -= 1


	# Step 2: Pick most likely for each level based on frequency
	# setup
	indents_final = {}

	for k,v in indents_probs.items():
		indents_final[k] =  max(set(v), key=v.count)


	# Step 3: Read line-by-line again and match against expectations
	# setup
	indents = 0
	current_line = 1 # line number counting starts at 1
	mixed_tabs_spaces_lines = []
	partly_wrong_lines = []
	wrong_lines = []

	# read line-by-line
	with open(sys.argv[f]) as source:
		for line in source:
			# get line indentation
			indentation = line[:len(line)-len(line.lstrip())] # read from beginning until start of stripped string
			if '\n' not in indentation: # must have been a newline if \n present after stripping, ignore

				# check for decrease indentation, only if non-code line with bracket is current line affected
				if line.strip().find('}') == 0: # decrease
					indents -= 1

				# check indentation against expectations and place error type
				if ('\t' in indentation and ' ' in indents_final[indents]) or (' ' in indentation and '\t' in indents_final[indents]):
					mixed_tabs_spaces_lines.append(current_line) # mixed tabs and spaces
				elif indentation != indents_final[indents]: # some other error
					for k,v in indents_final.items():
						if indentation == v and k != indents and current_line not in wrong_lines:
							wrong_lines.append(current_line) # fully wrong, at a different indent level
					if current_line not in wrong_lines: # most have only been partly wrong if didn't match any other level
						partly_wrong_lines.append(current_line)

				# check for indentation changes, '{' always affects next line and '}' affects next line if with code this line
				if '{' in line: # increase
					indents += 1
				if '}' in line and not line.strip().find('}') == 0: # decrease
					indents -= 1

			# always increment line counter
			current_line += 1

	# print report for current file
	total_lines = current_line # last line read is total line number
	total_mixed_tabs_spaces_lines = len(mixed_tabs_spaces_lines)
	total_partly_wrong_lines = len(partly_wrong_lines)
	total_wrong_lines = len(wrong_lines)

	string_mixed_tabs_spaces_lines = list_to_ranged_string(mixed_tabs_spaces_lines)
	string_partly_wrong_lines = list_to_ranged_string(partly_wrong_lines)
	string_wrong_lines = list_to_ranged_string(wrong_lines)

	blocks_mixed_tabs_spaces_lines = 0 if string_mixed_tabs_spaces_lines == '' else len(string_mixed_tabs_spaces_lines.split(','))
	blocks_partly_wrong_lines = 0 if string_partly_wrong_lines == '' else len(string_partly_wrong_lines.split(','))
	blocks_wrong_lines = 0 if string_wrong_lines == '' else len(string_wrong_lines.split(','))

	ratio_raw = (total_mixed_tabs_spaces_lines + total_partly_wrong_lines + total_wrong_lines) / float(total_lines)
	ratio_weighted = (WEIGHT_TABSPACE*total_mixed_tabs_spaces_lines
		+ WEIGHT_PARTLY*total_partly_wrong_lines
		+ WEIGHT_WRONG*total_wrong_lines) / float(total_lines)
	ratio_adjusted = (WEIGHT_TABSPACE*BLOCK_ADJUST(total_mixed_tabs_spaces_lines,blocks_mixed_tabs_spaces_lines)*total_mixed_tabs_spaces_lines
		+ WEIGHT_PARTLY*BLOCK_ADJUST(total_partly_wrong_lines,blocks_partly_wrong_lines)*total_partly_wrong_lines
		+ WEIGHT_WRONG*BLOCK_ADJUST(total_wrong_lines,blocks_wrong_lines)*total_wrong_lines) / float(total_lines)


	print("="*len(sys.argv[f]))
	print(sys.argv[f].upper())
	print("="*len(sys.argv[f]))
	print("Total Lines: " + str(total_lines))
	print("Total As Expected: " + str(total_lines - total_mixed_tabs_spaces_lines - total_partly_wrong_lines - total_wrong_lines))
	print("Total Unexpected: " + str(total_mixed_tabs_spaces_lines + total_partly_wrong_lines + total_wrong_lines))

	print("\nMixed Tabs/Spaces: " + str(total_mixed_tabs_spaces_lines) + " lines over " + str(blocks_mixed_tabs_spaces_lines) + " blocks")
	print("On Line Numbers: " + string_mixed_tabs_spaces_lines)

	print("\nIndentation Partly Wrong: " + str(total_partly_wrong_lines) + " lines over " + str(blocks_partly_wrong_lines) + " blocks")
	print("On Line Numbers: " + string_partly_wrong_lines)

	print("\nIndentation at Wrong Level: " + str(total_wrong_lines) + " lines over " + str(blocks_wrong_lines) + " blocks")
	print("On Line Numbers: " + string_wrong_lines)

	print("\nRatios (lower is preferred):")
	print("Raw: {0:.2f}%".format(ratio_raw*100))
	print("Weighted: {0:.2f}%".format(ratio_weighted*100))
	print("Adjusted: {0:.2f}%".format(ratio_adjusted*100))
	print("")

	file_lines.append(total_lines)
	if BLOCK_LEVEL:
		file_ratios.append(ratio_adjusted)
	else:
		file_ratios.append(ratio_weighted)


# Final report
if FILE_WEIGHT:
	final_ratio = sum([x/float(sum(file_lines)) * y for x,y in zip(file_lines,file_ratios)])
else:
	final_ratio = sum(file_ratios)/float(len(file_ratios))

final_ratio = final_ratio * 100; # scale by 100 to get percentage from decimal score

if final_ratio < 8:
	feedback = "There may be a few minor indentation errors (see notes above) but no major issues."
	score = 100
elif final_ratio < 20:
	feedback = "There were a few major or several minor indentation errors (see notes above)"
	score = 75
elif final_ratio < 35:
	feedback = "There were several major indentation errors (see notes above)"
	score = 50
else:
	feedback = "There were many major indentation errors (see notes above)"
	score = 25

print("==================================")
print("Overall Improper Indentation Rate: {0:.2f}%".format(final_ratio))
print("Feedback: " + feedback)
print(score)
