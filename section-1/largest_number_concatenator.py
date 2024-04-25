#!/usr/bin/python3

def printLargest(arr):
    """
    takes the array of strings arr[] as a parameter and returns a string
    denoting the answer
    """
    n = len(arr)

    # Using bubble sort algorithm
    for i in range(n):
        for j in range(0, n-i-1):
            if int(arr[j] + arr[j+1]) < int(arr[j+1] + arr[j]):
                """
                check if output of concatenating string is less than
                concatenating in the reverse order, swap them if true
                """
            arr[j], arr[j+1] = arr[j+1], arr[j]

    output = ''.join(arr)
    return output
