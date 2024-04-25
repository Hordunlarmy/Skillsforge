#!/usr/bin/python3

def compress(string):
    """ Compress a string """

    if not string:
        return string

    compressed = []
    current = string[0]
    no_of_char = 0

    for char in string:
        if char == current:
            no_of_char += 1
        else:
            if no_of_char > 1:
                compressed.append(current + str(no_of_char))
            else:
                compressed.append(current)
            current = char
            no_of_char = 1

    # Handling the last sequence
    if no_of_char > 1:
        compressed.append(current + str(no_of_char))
    else:
        compressed.append(current)

    compressed_string = ''.join(compressed)

    if len(compressed_string) < len(string):
        return compressed_string
    else:
        return string


# Test cases
assert compress('bbcceeee') == 'b2c2e4'
assert compress('aaabbbcccaaa') == 'a3b3c3a3'
assert compress('a') == 'a'
print("All tests passed successfully!")
