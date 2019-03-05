# C++ Static Analysis Scripts

_A collection of python scripts for static analysis of C++ code_

## README

### Overview

I was using an auto-grading system called [Mimir Classroom](https://www.mimirhq.com) for introductory C++ labs last semester, and while I like the speed and capability of auto-graders, I found that it still takes a bit of time to review code and give meaningful feedback to students about readability, design, etc.

To save time on some rubric items, I looked into linters and style checkers but found most of them too pedantic.  I felt some simple techniques would be enough to evaluate most of the points I cared about, so I wrote a few analysis scripts in python to check C++ code statically.  The next section discusses each of the scripts in a little more detail.

### Scripts

#### Commenting

The `check_commenting.py` script uses a simple comment-to-code ratio to determine effective usage of comments.  It counts up all lines of code and all lines of comments, with support for single and multi-line comments.  Then it takes the ratio.  While there is no industry standard for a good comment-to-code ratio, 30% is a well-liked number, and it seems very reasonable to me for an introductory class.  Students can write fewer comments in later classes, but I think it's important to enforce commenting when they are just beginning.

#### Indentation Consistency

Another "style" element; the compiler may not care about C++ indentation, but students should try to write readable code.  The script `check_indentation.py` checks all the lines of code and selects the indentation of each level using a majority selector.  That is, it selects the most frequent indentation seen for a given level as the desired number of tabs or spaces and then compares how many lines disagree with the most common indentation for any level.  The penalty for completely missing an indentation, having in-between indentation, or mixing tabs and spaces can be adjusted with individual weights.

#### Expression Complexity

Starting with `check_expressions.py`, the scripts are less about style and more about design.  It's tricky to automatically evaluate topics like good abstraction and complexity without very advanced algorithms, but if you accept some limitations, there are certain indicators of these broader ideas which can be easily observed.  In this instance, we are looking at conditional statements.  If the conditional logic is long or makes extensive use of compound operators like `&&` or `||`, the students are likely writing out a lot of unnecessary code instead of developing cleaner, more readable code.  This metric is based off my own review of students' programs, so it may vary.  Accordingly, the specific weights and thresholds for determining long expressions can be adjusted.

#### Meaningful Variables

The `check_variables.py` script is intended to check if students are writing code with useful variables, e.g. naming something like `player_name` as opposed to `x`.  This is also a difficult problem, so I use a simple proxy: length of common data type declarations.  Looking only at the most basic C/C++ data types (int, char, bool, ...), one can easily check the length of variable names when first declared.  If a lot of variables have short names, students are probably just using letters or something equally meaningless.  However, given that short names can still have meaning, I do think this is the most arguable metric.  To give it a little more value, I added looking at scope of variables in `for` loops.  It prefers that counters and other looping variables be declared at the start of the loop.  All of these weights and thresholds can be changed as desired.

#### Abstraction

Good abstraction and design is the hardest problem broached in these scripts.  It is difficult to evaluate objectively even from a human's perspective, but I believe a reasonable indicator is repeating code.  If a student is repeating a lot of code, it's vary likely bad abstraction.  Although it's not true that non-repeating code always has good abstraction, it seems a sensible enough measure for an introductory class.  The `check_repetition.py` script reviews all the lines of code, finds complete matches, and then uses difflib to search for similar lines.  All of the weights and thresholds can be changed.

### Usage

The scripts are meant to be altered as needed.  Each description mentions that weights and thresholds can be easily altered.  These appear at the top of scripts as global (all caps) variables.  They are weights, thresholds, equations, or anything else which could vary depending on the specific task.  For example, I apply a small penalty for mixing tabs and spaces, but this could be weighted to 0 if you don't care about such a minor mistake.

Each script is intended to be invoked with python, passing the files to check as command line arguments.  To search for lengthy expressions in `main.cpp`:

```
python check_expressions.py main.cpp
```

Any number of files can be passed in, including wildcards:

```
python check_indentation.py main.cpp LinkedList.h LinkedList.cpp
```

```
python check_repetition.py *.cpp
```

The output is currently in Mimir's preferred format, comprising of a number from 0 to 100, corresponding with 0% to 100% credit for that test.  If you look at the bottom of each file, the values and associated scores can all be changed directly.  As I mentioned before, I like the idea of code being around 30% comment-to-code ratio, but give anywhere from 18% to 50% full credit.  The ratios, scores, and feedback could all be edited to suggest a different comment-to-code rate.

## License

I grant anyone permission to use whatever parts of these scripts and associated files they want for any purpose, free of charge and without warranty.  You don't need to include attribution or open-source derivative works unless you wish.  I hope these prove useful to someone!
