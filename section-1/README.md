# 1. String Compression

## Overview
The String Compression provides a simple yet efficient way to compress a string by reducing sequences of the same character to that character followed by the number of its occurrences. This utility is particularly useful for reducing the size of long strings where many characters are repeat consecutively.

## Functionality
- **Compress Function**: Takes a single string as input and returns a compressed version of the string where each group of consecutive identical characters is replaced by the character followed by the number of occurrences. If the compressed string is not shorter than the original, the original string is returned unchanged.

## Usage

### Requirements
Ensure you have Python installed on your system. This utility was developed and tested with Python 3.8, but it should work with any Python 3.x version.

### Installing
No installation is necessary. You can include the `compress.py` file in your project directory and import the function directly.

### Examples
Here are a few examples of how to use the `string_compression` function:

```python
from string_compression import compress

# Example 1
original_string = "bbcceeee"
compressed_string = compress(original_string)
print(compressed_string)  # Output: b2c2e4

# Example 2
original_string = "aaaabbbccddddddee"
compressed_string = compress(original_string)
print(compressed_string)  # Output: a4b3c2d6e2

# Example 3
original_string = "a"
compressed_string = compress(original_string)
print(compressed_string)  # Output: a
```

# 2. Largest Number Concatenator

## Overview
This Largest number concatenator provides a solution to the problem of arranging a given array of string representations of non-negative integers in such a manner that, when concatenated in order, they form the largest possible number. This implementation leverages a custom sorting algorithm to maximize the concatenated result.

## Functionality
- **Custom Sorting Algorithm**: Implements a bubble sort with a special comparator that considers the best concatenation of numbers.
Efficiency: Direct and straightforward implementation suitable for small to medium-sized datasets.

## Usage

### Requirements
This script is written in Python 3 and does not require any external libraries. It runs with the standard Python installation.

### Installing
No installation is necessary. You can include the `compress.py` file in your project directory and import the function directly.

### Examples
Here are a few examples of how to use the `largest_number_concatenator` function:

```python
from largest_number_concatenator import printLargest

# Example 1
arr = ["3", "30", "34", "5", "9"]
output = printLargest(arr)
print(output) # Output: "9534330"

# Example 2
arr = ["54", "546", "548", "60"]
output = printLargest(arr)
print(output) # Output: "6054854654"
```
