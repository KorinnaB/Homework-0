#!/usr/bin/env python3
"""
- Reads file1 and file2 once, storing their integers in memory
- Computes the sum of integers in each file
- If sums are equal, file2 comes first by this implementation
- Make it work with integer values (zero, positive, negative)
- Make it so input files must cotain one integer per line
- double check it works on linux
"""

import sys

def read_file(filename):
    numbers = []
    total = 0
    with open(filename, "r") as f:
        for line in f:
            num = int(line.strip())
            numbers.append(num)
            total += num
    return numbers, total

def write_file(filename, list1, list2):
    with open(filename, "w") as f:
        for num in list1 + list2:
            f.write(str(num) + "\n")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("To Combine Use: python combine_files.py <file1> <file2> [file3]")
        print("If no [file3] is not provided a file called myoutput.txt will be created")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    file3 = sys.argv[3] if len(sys.argv) == 4 else "myoutput.txt"

    list1, sum1 = read_file(file1)
    list2, sum2 = read_file(file2)

    if sum1 < sum2:
        write_file(file3, list1, list2)
    elif sum2 < sum1:
        write_file(file3, list2, list1)
    else:
        write_file(file3, list1, list2)

    print(f"Merge Complete! Output written to {file3}")

if __name__ == "__main__":
    main()