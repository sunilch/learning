# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

bestPalindromDict={}

def bestPalindromeOf(inptext):
    '''returns the best subset Palindrome in the middle of the string'''
    global bestPalindromDict
    if len(inptext)==1: return inptext
    if len(inptext)==2 and inptext[0]==inptext[-1]: return inptext
    if len(inptext)==2 and inptext[0]!=inptext[-1]: return inptext[0]
    if inptext not in bestPalindromDict:
        bestPalindromDict[inptext]=inptext if inptext[0]==inptext[-1] and bestPalindromeOf(inptext[1:-1])==inptext[1:-1] \
            else bestPalindromeOf(inptext[1:-1])
    return bestPalindromDict[inptext]

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    # Your code here
    if text=='':return (0,0)
    text=text.lower()
    bestSubsetPalindrome=max((bestPalindromeOf(text[start:end]) for start in range(len(text))
                             for end in range(start+1,len(text)+1)),key=len)
    return (text.find(bestSubsetPalindrome),text.find(bestSubsetPalindrome)+len(bestSubsetPalindrome))

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()