
"""This file contains a bunch of different prompts for the agents. """

#---------------------ZERO-SHOT AGENT PROMPTS---------------------------

PROGRAMMER_PROMPT = """
**Role**: You are an expert programmer.

**Task**: Your task is to write code that solves the given problem. 

**Code Formatting**: Please write code in 
```python
[Code]
``` 
format.

*Encapsulate the input/output in a main() function to separate the core logic from the script execution.* 
*Write all needed imported modules at the top*
*Use the function input() to read the input*

"""

TEST_DESIGNER_PROMPT= """ 
**Role**: As a tester, your task is to create comprehensive test cases for a function named main(). 
It reads input from input() and outputs results to `stdout`. Use `@patch` decorator to mock `input` and `stdout`
, and ensure the test compares the output with the expected result using `self.assertEqual`.

- The format of each test cases should be:
```python
    @patch('builtins.input', side_effect=['sample_input_line_1', 'sample_input_line_2', '...'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_sample_input_1(self, mock_stdout, mock_input):
        # Call the function that uses input() and print()
        main()
        
        # Assert that the entire output matches the expected output
        self.assertEqual(mock_stdout.getvalue().strip(), 'expected_output_line_1\nexpected_output_line_2\n...')     
```

- The imports needed are:
```python
import unittest
from unittest.mock import patch
from io import StringIO
```

**For the test cases based on the Sample inputs make sure that the `side_effect` list contains only the input lines provided in the Sample Inputs.
**Make use of the unittest mock module to mock user input and print.**
**Do not import local modules for example: `your_module`. Because the `main` function will be inserted later to the script.**

*Code* 
{code} 

*Problem* 
{problem} 

"""

DEBUGGER_PROMPT = """ 
**Role**: You are an expert programmer.
**Task**: Identify what is wrong with the Code by analyzing the Code, Error and Tests. Then fix the Code and ensure that the it solves the given Problem description. 
The test cases show sampled input and output pairs, with side_effect being the sample input and the second parameter in self.assertEqual being the sample output. 

**Debugged Code Formatting**: Please write the fixed code in 
```python
[Code]
``` 
format.

*Find what causes the error, explain step by step how to fix it and then fix it.*
*Ensure to return the fixed Code in one Python codeblock *
*If necessary, implement a new logic to fit the problem*
*Write all needed imported modules at the top*
*Do not write or modify any test cases*

Please re-write the code to fix the bug and return only the fixed Code.

Problem description.
{problem} 

Previous version: 
{code}. 

Error: 
{error}. 

Test Cases: 
{tests}. 
                                    
"""


#---------------------------------APPS DATASET TASKS EXAMPLES-----------------------------

APPS_TASK_1 = '''
An accordion is a string (yes, in the real world accordions are musical instruments, but let's forget about it for a while) 
which can be represented as a concatenation of: an opening bracket (ASCII code $091$), a colon (ASCII code $058$), 
some (possibly zero) vertical line characters (ASCII code $124$), another colon, and a closing bracket (ASCII code $093$). 
The length of the accordion is the number of characters in it. For example, [::], [:||:] and [:|||:] are accordions having length 
$4$, $6$ and $7$. (:|:), {{:||:}} , [:], ]:||:[ are not accordions. 

You are given a string $s$. You want to transform it into an accordion by removing some (possibly zero) characters from it. Note that you may not insert new characters or reorder existing ones. 
Is it possible to obtain an accordion by removing characters from $s$, and if so, what is the maximum possible length of the result? 

-----Input----- 
The only line contains one string $s$ ($1 \le |s| \le 500000$). 
It consists of lowercase Latin letters and characters [, ], : and |. 

-----Output----- 
If it is not possible to obtain an accordion by removing some characters from $s$, print $-1$. 
Otherwise print maximum possible length of the resulting accordion. 

-----Examples----- 
Sample Input 1 
|[a:b:|] 

Sample Output 1
4 

Sample Input 2
|]:[|:] 

Sample Output 2
-1

'''



APPS_TASK_1_CODE = """
```python
def main():
    # Take user input and assign it to the variable 's'
    s = input()

    # Calculate the length of the string 's' and assign it to the variable 'n'
    n = len(s)

    # Initialize variables to store the indices of '[' and ']'
    ind = -1
    bind = -1

    # Variable to track whether '[' or ']' characters have been encountered
    f = False

    # Step 1: Find the index of the first '[' character after encountering ':'
    for i in range(n):
        if s[i] == '[':
            f = True
        elif s[i] == ':':
            if f:
                ind = i
                break

    # Reset the flag variable
    f = False

    # Step 2: Find the index of the last ']' character before encountering ':'
    for i in range(n - 1, -1, -1):
        if s[i] == ']':
            f = True
        elif s[i] == ':':
            if f:
                bind = i
                break

    # Check conditions to determine if it's possible to obtain an accordion
    if ind == -1 or bind == -1:
        # Print -1 if '[' or ']' characters were not found
        print(-1)
    elif ind >= bind:
        # Print -1 if the order of '[' and ']' characters is incorrect
        print(-1)
    else:
        # Initialize the length of the accordion to 4 (opening and closing brackets, and two colons)
        ans = 4
        # Step 3: Count the number of '|' characters between '[' and ']' indices (inclusive)
        for i in range(ind + 1, bind):
            if s[i] == '|':
                ans += 1
        # Print the calculated length of the resulting accordion
        print(ans)
if __name__ == '__main__':
    main()
```
"""

APPS_TASK_1_TESTS = """
```python
import unittest
from unittest.mock import patch
from io import StringIO

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['|[a:b:|]'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_1(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '4')

    @patch('builtins.input', side_effect=['|]:[|:]'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_2(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '-1')

    @patch('builtins.input', side_effect=[':][:'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_3(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '-1')

    @patch('builtins.input', side_effect=[':[]:'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_4(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '-1')

    @patch('builtins.input', side_effect=['[[:]]'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_5(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '-1')

if __name__ == '__main__':
    unittest.main()
```
"""

APPS_TASK_1_BUG = """
```python
import unittest
from unittest.mock import patch
from io import StringIO


def main():
    # Take user input and assign it to the variable 's'
    s = input()

    # Calculate the length of the string 's' and assign it to the variable 'n'
    n = len(s)

    # Initialize variables to store the indices of '[' and ']'
    ind = -1
    bind = -1

    # Variable to track whether '[' or ']' characters have been encountered
    f = False

    # Step 1: Find the index of the first '[' character after encountering ':'
    for i in range(n):
        if s[i] == '[':
            f = True
        elif s[i] == ':':
            if f:
                ind = i
                break

    # Reset the flag variable
    f = False

    # Step 2: Find the index of the last ']' character before encountering ':'
    for i in range(n - 2, -1, -1): 
        if s[i] == ']':
            f = True
        elif s[i] == ':':
            if f:
                bind = i
                break

    # Check conditions to determine if it's possible to obtain an accordion
    if ind == -1 or bind == -1:
        # Print -1 if '[' or ']' characters were not found
        print(-1)
    elif ind >= bind:
        # Print -1 if the order of '[' and ']' characters is incorrect
        print(-1)
    else:
        # Initialize the length of the accordion to 4 (opening and closing brackets, and two colons)
        ans = 4
        # Step 3: Count the number of '|' characters between '[' and ']' indices (inclusive)
        for i in range(ind + 1, bind):
            if s[i] == '|':
                ans += 1
        # Print the calculated length of the resulting accordion
        print(ans)

if __name__ == "__main__":
    main()
```
"""

APPS_ERROR_1 = """
FAIL: test_case_1 (__main__.TestMain)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/claudia/miniconda3/envs/langgraph2/lib/python3.10/unittest/mock.py", line 1379, in patched
    return func(*newargs, **newkeywargs)
  File "/mnt/c/Users/Claudia/Desktop/KTH/MEX/MEX2024/test.py", line 66, in test_case_1
    self.assertEqual(mock_stdout.getvalue().strip(), '4')
AssertionError: '-1' != '4'
- -1
+ 4
"""

APPS_TASK_2= """

Anton has the integer x. He is interested what positive integer, which doesn't exceed x, has the maximum sum of 
digits. Your task is to help Anton and to find the integer that interests him. If there are several such integers, 
determine the biggest of them. 

-----Input-----
The first line contains the positive integer x (1 ≤ x ≤ 10^18) — the integer which Anton has. 


-----Output-----
Print the positive integer which doesn't exceed x and has the maximum sum of digits. If there are several such integers, print the biggest of them. Printed integer must not contain leading zeros.


-----Examples-----
Sample Input 1
100

Sample Output 1
99

Sample Input 2
48

Sample Output 2
48

Sample Input 3
521

Sample Output 3
499

"""




APPS_TASK_2_CODE = """

```python
def main():
    # Take user input as a list of integers representing the digits of the given positive integer x
    num = list(map(int, input()))

    # Initialize a variable 'best' to store the current best candidate for the maximum sum of digits
    best = num[:]

    # Step 1: Iterate over the digits in reverse order
    for i in range(-1, -len(num) - 1, -1):
        # If the current digit is 0, continue to the next digit
        if num[i] == 0:
            continue
        
        # Decrease the current digit by 1
        num[i] -= 1

        # Step 2: Set all digits to the right of the current digit to 9
        for j in range(i + 1, 0):
            num[j] = 9
        
        # Step 3: Compare the sum of the current number with the sum of the best number
        if sum(num) > sum(best):
            # Update 'best' if the current number has a greater sum
            best = num[:]

    # Convert the list of digits to a string, remove leading zeros, and print the result
    s = ''.join(map(str, best)).lstrip('0')
    print(s)

if __name__ == '__main__':
    main()
```

"""

APPS_TASK_2_TESTS = """
```python
import unittest
from unittest.mock import patch
from io import StringIO

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['100'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_1(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '99')

    @patch('builtins.input', side_effect=['48'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_2(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '48')

    @patch('builtins.input', side_effect=['521'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_3(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '499')

    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_4(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '1')

    @patch('builtins.input', side_effect=['2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_5(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '2')

if __name__ == '__main__':
    unittest.main()
```
"""

APPS_TASK_2_BUG = """
```python
def main():
    # Take user input as a list of integers representing the digits of the given positive integer x
    num = list(map(int, input()))

    # Initialize a variable 'best' to store the current best candidate for the maximum sum of digits
    best = num[:]

    # Step 1: Iterate over the digits in reverse order
    for i in range(-1, -len(num) - 1, -1):
        # If the current digit is 0, continue to the next digit
        if num[i] == 0:
            continue
        
        # Decrease the current digit by 1
        num[i] += 1 

        # Step 2: Set all digits to the right of the current digit to 9
        for j in range(i + 1, 0): 
            num[j] = 9
        
        # Step 3: Compare the sum of the current number with the sum of the best number
        if sum(num) > sum(best):
            # Update 'best' if the current number has a greater sum
            best = num[:]

    # Convert the list of digits to a string, remove leading zeros, and print the result
    s = ''.join(map(str, best)).lstrip('0')
    print(s)

if __name__ == "__main__":
    main()
```

"""

APPS_ERROR_2 = """
Traceback (most recent call last):
  File "/home/claudia/miniconda3/envs/langgraph2/lib/python3.10/unittest/mock.py", line 1379, in patched
    return func(*newargs, **newkeywargs)
  File "/mnt/c/Users/Claudia/Desktop/KTH/MEX/MEX2024/test.py", line 64, in test_case_5
    self.assertEqual(mock_stdout.getvalue().strip(), '2')
AssertionError: '3' != '2'
- 3
+ 2

"""

APPS_TASK_3 = """

Apart from having lots of holidays throughout the year, residents of Berland also have whole lucky years. 
Year is considered lucky if it has no more than 1 non-zero digit in its number. So years 100, 40000, 5 are lucky
and 12, 3001 and 12345 are not. You are given current year in Berland. Your task is to find how long will residents 
of Berland wait till the next lucky year.

-----Input-----
The first line contains integer number n (1 ≤ n ≤ 10^9) — current year in Berland.

-----Output-----
Output amount of years from the current year to the next lucky one.

-----Examples-----
Sample Input 1
4

Sample Output 1
1

Sample Input 2
201

Sample Output 2
99

Sample Input 3
4000

Sample Output 3
1000

"""

APPS_TASK_3_CODE = """

```python
def main():
    # Take user input as a string representing the current year in Berland
    s = input()

    # Get the length of the input string (number of digits in the current year)
    n = len(s)

    # Step 1: Create a target lucky year 't' by incrementing the first digit by 1 and padding with zeros
    t = int(str(int(s[0]) + 1) + '0' * (n - 1))

    # Step 2: Calculate the number of years from the current year to the next lucky one
    result = t - int(s)

    # Print the result
    print(result)

if __name__ == '__main__':
    main()
```

"""


APPS_TASK_3_TESTS = """
```python
import unittest
from unittest.mock import patch
from io import StringIO

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['4'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_1(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '1')

    @patch('builtins.input', side_effect=['201'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_2(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '99')

    @patch('builtins.input', side_effect=['4000'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_3(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '1000')

    @patch('builtins.input', side_effect=['9'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_4(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '1')

    @patch('builtins.input', side_effect=['10'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_5(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), '10')

if __name__ == '__main__':
    unittest.main()
```
"""

##Solution for APPS_TASK3_BUG: The error lies on row 12, it should be t - int(s) not t + int(s)\n
APPS_TASK_3_BUG = """
```python
def main():
    # Take user input as a string representing the current year in Berland
    s = input()

    # Get the length of the input string (number of digits in the current year)
    n = len(s)

    # Step 1: Create a target lucky year 't' by incrementing the first digit by 1 and padding with zeros
    t = int(str(int(s[0]) + 1) + '0' * (n - 1))

    # Step 2: Calculate the number of years from the current year to the next lucky one
    result = t + int(s)

    # Print the result
    print(result)

if __name__ == "__main__":
    main()
```

"""

APPS_ERROR_3 = """
Traceback (most recent call last):
  File "/home/claudia/miniconda3/envs/langgraph2/lib/python3.10/unittest/mock.py", line 1379, in patched
    return func(*newargs, **newkeywargs)
  File "/mnt/c/Users/Claudia/Desktop/KTH/MEX/MEX2024/test.py", line 27, in test_case_1
    self.assertEqual(mock_stdout.getvalue().strip(), '1')
AssertionError: '9' != '1'
- 9
+ 1

"""

APPS_TASK_4 = """ ""
Polycarp has recently created a new level in this cool new game Berlio Maker 85 and uploaded it online. Now players from all over the world can try his level. 
All levels in this game have two stats to them: the number of plays and the number of clears. So when a player attempts the level, the number of plays increases by $1$. 
If he manages to finish the level successfully then the number of clears increases by $1$ as well. 
Note that both of the statistics update at the same time (so if the player finishes the level successfully then the number of plays will increase at the same time as the number of clears). 
Polycarp is very excited about his level, so he keeps peeking at the stats to know how hard his level turns out to be. 
So he peeked at the stats $n$ times and wrote down $n$ pairs of integers — $(p_1, c_1), (p_2, c_2), \dots, (p_n, c_n)$, where $p_i$ is the number of plays at the $i$-th moment of time and $c_i$ is the number of clears at the same moment of time. 
The stats are given in chronological order (i.e. the order of given pairs is exactly the same as Polycarp has written down). Between two consecutive moments of time Polycarp peeked at the stats many players (but possibly zero) could attempt the level. 
Finally, Polycarp wonders if he hasn't messed up any records and all the pairs are correct. If there could exist such a sequence of plays (and clears, respectively) that the stats were exactly as Polycarp has written down, then he considers his records correct. 
Help him to check the correctness of his records. For your convenience you have to answer multiple independent test cases. 

-----Input----- 
The first line contains a single integer $T$ $(1 \le T \le 500)$ — the number of test cases. 
The first line of each test case contains a single integer $n$ ($1 \le n \le 100$) — the number of moments of time Polycarp peeked at the stats. 
Each of the next $n$ lines contains two integers $p_i$ and $c_i$ ($0 \le p_i, c_i \le 1000$) — the number of plays and the number of clears of the level at the $i$-th moment of time. 
Note that the stats are given in chronological order. 

-----Output----- For each test case print a single line. 
If there could exist such a sequence of plays (and clears, respectively) that the stats were exactly as Polycarp has written down, 
then print "YES". Otherwise, print "NO". You can print each letter in any case (upper or lower).
-----Examples-----
Sample Input 1
6\n3\n0 0\n1 1\n1 2\n2\n1 0\n1000 3\n4\n10 1\n15 2\n10 2\n15 2\n1\n765 432\n2\n4 4\n4 3\n5\n0 0\n1 0\n1 0\n1 0\n1 0\n

Sample Output 1
NO\nYES\nNO\nYES\nNO\nYES\n

Sample Input 2
1\n2\n10 1\n11 3\n

Sample Output 2
NO\n

Sample Input 3
1\n2\n5 2\n8 6\n

Sample Output 3
NO\n




"""

APPS_TASK_4_CODE = """
```python
import sys
from math import gcd
from collections import defaultdict
from copy import copy

# Input reading functions
R = lambda t=int: t(input())
RL = lambda t=int: [t(x) for x in input().split()]
RLL = lambda n, t=int: [RL(t) for _ in range(n)]

def solve():
    n = R()
    S = RLL(n)
    lp, lc = 0, 0
    for p, c in S:
        if lp > p or lc > c or c - lc > p - lp:
            print('NO')
            return
        lp, lc = p, c
    print('YES')

def main():
    T = R()
    for _ in range(T):
        solve()

if __name__ == "__main__":
    main()
```
"""

APPS_TASK_4_TESTS= """
```python
import unittest
from unittest.mock import patch
from io import StringIO

class TestSolution(unittest.TestCase):

    @patch('builtins.input', side_effect=['6', '3', '0 0','1 1','1 2','2','1 0','1000 3','4','10 1','15 2','10 2','15 2','1','765 432','2','4 4','4 3','5','0 0','1 0','1 0','1 0','1 0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_1(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'NO\nYES\nNO\nYES\nNO\nYES')

    @patch('builtins.input', side_effect=['1','2','10 1','11 3'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_2(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'NO')

    @patch('builtins.input', side_effect=['1','2','5 2','8 6'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_case_3(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'NO')

if __name__ == "__main__":
    unittest.main()
```
"""

#Error caused by line 19. Should be lp, lc = p, c. 
APPS_TASK_4_BUG = """
```python
import sys
from math import gcd
from collections import defaultdict
from copy import copy

# Input reading functions
R = lambda t=int: t(input())
RL = lambda t=int: [t(x) for x in input().split()]
RLL = lambda n, t=int: [RL(t) for _ in range(n)]

def solve():
    n = R()
    S = RLL(n)
    lp, lc = 0, 0
    for p, c in S: 
        if lp > p or lc > c or c - lc > p - lp:  
            print('NO') 
            return
        lp, lc = p, lp 
    print('YES')

def main():
    T = R()
    for _ in range(T):
        solve()

if __name__ == "__main__":
    main()
```

"""

APPS_ERROR_4 = """
Traceback (most recent call last):
  File "/home/claudia/miniconda3/envs/langgraph2/lib/python3.10/unittest/mock.py", line 1379, in patched
    return func(*newargs, **newkeywargs)
  File "/mnt/c/Users/Claudia/Desktop/KTH/MEX/MEX2024/test.py", line 37, in test_case_1
    self.assertEqual(mock_stdout.getvalue().strip(), 'NO\nYES\nNO\nYES\nNO\nYES')
AssertionError: 'NO\nYES\nNO\nYES\nNO\nNO' != 'NO\nYES\nNO\nYES\nNO\nYES'
  NO
  YES
  NO
  YES
  NO
- NO+ YES

"""

#----------------------------Chain-of-Thought (CoT)--------------------------------------
PROGRAMMER_COT_PROMPT = """

**Role**: You are an expert programmer.

**Task**: Your task is to write code that solves the given problem. Follow a step-by-step Chain of Thought process to break down the problem, create pseudocode, and then write the code in Python.

**Code Formatting**: Please write code in 
```python
[Code]
``` 
format.

*Encapsulate the input/output in a main() function to separate the core logic from the script execution.* 
*Write all needed imported modules at the top*
*Use the function input() to read the input*

# For example:

##Problem 1: \n""" +  APPS_TASK_1 + "\n##Solution 1: \n" + APPS_TASK_1_CODE + "\n##Problem 2: \n" + APPS_TASK_2 + "\n##Solution 2: \n" + APPS_TASK_2_CODE + "\n##Problem 3: \n" + APPS_TASK_4 + "\n##Solution 3: \n" + APPS_TASK_4_CODE



TEST_DESIGNER_COT_PROMPT = """
**Role**: As a tester, your task is to create comprehensive test cases for a function named main(). 
It reads input from input() and outputs results to `stdout`. Use `@patch` decorator to mock `input` and `stdout`
, and ensure the test compares the output with the expected result using `self.assertEqual`.

- The format of each test cases should be:
```python
    @patch('builtins.input', side_effect=['sample_input_line_1', 'sample_input_line_2', '...'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_sample_input_1(self, mock_stdout, mock_input):
        # Call the function that uses input() and print()
        main()
        
        # Assert that the entire output matches the expected output
        self.assertEqual(mock_stdout.getvalue().strip(), 'expected_output_line_1\nexpected_output_line_2\n...')     
```

- The imports needed are:
```python
import unittest
from unittest.mock import patch
from io import StringIO
```

**For the test cases based on the Sample inputs make sure that the `side_effect` list contains only the input lines provided in the Sample Inputs.
**Make use of the unittest mock module to mock user input and print.**
**Do not import local modules for example: `your_module`. Because the `main` function will be inserted later to the script.**

# For example:

##Example 1:\n Code\n""" + APPS_TASK_1_CODE + "\nProblem\n" + APPS_TASK_1 +"\n## Generated tests 1:\n" + APPS_TASK_1_TESTS + "\n##Example 2:\n Code\n" + APPS_TASK_2_CODE + "\n Problem \n" + APPS_TASK_2 + "\n## Generated tests 2:\n" + APPS_TASK_2_TESTS + "\n##Example 3:\n Code\n" + APPS_TASK_4_CODE + "\nProblem\n" + APPS_TASK_4 + "\n## Generated tests 3:\n" + APPS_TASK_4_TESTS + """

*Code* 
{code} 

*Problem* 
{problem}  
 
"""

DEBUGGER_COT_PROMPT = """
**Role**: You are an expert programmer.
**Task**: Identify what is wrong with the Code by analyzing the Code, Error and Tests. Then fix the Code and ensure that the it solves the given Problem description. 
The test cases show sampled input and output pairs, with side_effect being the sample input and the second parameter in self.assertEqual being the sample output. 

**Debugged Code Formatting**: Please write the fixed code in 
```python
[Code]
``` 
format.

*Find what causes the error, explain step by step how to fix it and then fix it.*
*Ensure to return the fixed Code in one Python codeblock *
*If necessary, implement a new logic to fit the problem*
*Write all needed imported modules at the top*
*Do not write or modify any test cases*


# For example:

##Example 1\n: \n Previous Code \n""" +  APPS_TASK_1_BUG + "\n Error\n" + APPS_ERROR_1 + "\n Tests\n" + APPS_TASK_1_TESTS  + "\n##Solution 1: # The error is caused by the for loop in row 27, it should by for i in range (n-1, -1, -1). Fixed code: \n" + APPS_TASK_1_CODE + "\n##Example 2\nPrevious Code \n " + APPS_TASK_2_BUG + "\n Error\n" + APPS_ERROR_2 + "\n Tests\n"  +"\n##Solution 2: The error lies on row 15, the current digit num[i] should be decreased by 1 not increased by 1. \n" + APPS_TASK_2_CODE + "\n##Example 3:\nPrevious Code\n" + APPS_TASK_4_BUG + "\n Error\n" + APPS_ERROR_4 + "\n Tests\n" + APPS_TASK_4_TESTS + "\n##Solution 3: The error lies on row 19. It should be lp, lc = p, c.\n " + APPS_TASK_4_CODE + """

Please re-write the code to fix the bug and return only the fixed Code.

*Problem Description:*  
{problem}

*Previous Code:* 
{code}

*Error:*
{error}

*Tests:*
{tests}

"""

