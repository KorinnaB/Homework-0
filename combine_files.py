#!/usr/bin/env python3

"""
CSCI4406 - Fall 25
Korinna B., Charisma R., Allison H., Emma W.
- Reads file1 and file2 once, storing their integers in memory
- Computes the sum of integers in each file
- If sums are equal, file2 comes first by this implementation
- Make it work with integer values (zero, positive, negative)
- Make it so input files must cotain one integer per line
"""

import sys

def read_file(filename): 
    numbers = [] # list to store integers
    total = 0 # stores sum of integers 
    with open(filename, "r") as f: # opens file in read mode
        for line in f:
            num = int(line.strip())
            numbers.append(num) # stores integer values in numbers
            total += num # adds integers to sum
    return numbers, total

def write_file(filename, list1, list2): 
    with open(filename, "w") as f:
        for num in list1 + list2: # concatenates lists
            f.write(str(num) + "\n") # writes integer values to file sep by newline

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4: # checks num of arguments from cli passed to script
        print("To Combine Use: python combine_files.py <file1> <file2> [file3]")
        print("If no [file3] is provided a file called myoutput.txt will be created")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2] # assigns file1 and file2 to first two cli arguments
    file3 = sys.argv[3] if len(sys.argv) == 4 else "myoutput.txt" # if no file3 was provided then myoutput.txt

    list1, sum1 = read_file(file1)
    list2, sum2 = read_file(file2)

# compares sums of lists, file w smaller sum gets printed first
    if sum1 < sum2: 
        write_file(file3, list1, list2)
    elif sum2 < sum1:
        write_file(file3, list2, list1)
    else:
        write_file(file3, list1, list2)

    print(f"Merge Complete! Output written to {file3}")

if __name__ == "__main__":
    main()
