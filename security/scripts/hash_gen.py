import itertools
import string
import sys
from hashlib import sha1

def genHash(password):
    hash = "*" + sha1(sha1(password.encode('utf-8')).digest()).hexdigest().upper()
    return hash

def genCombinations(dictionary, nr_elements):
    return list(itertools.combinations(dictionary, nr_elements))

try:
    NR_CHARS = int(sys.argv[1])
except IndexError:
    print("Syntax: " + sys.argv[0] + " <nr_of_characters>")
    sys.exit(2)

'''
This thing generates this amount of data:
6,2M -> file with combinations of dictio taken in groups of 3
143M -> file with combinations of dictio taken in groups of 4
2,6G -> file with combinations of dictio taken in groups of 5
'''
dictio = string.ascii_letters + string.digits + string.punctuation
combos =genCombinations(dictio, NR_CHARS)
for index in range(len(combos)):
    string_combo = ''
    for char in list(combos[index]):
        string_combo += str(char)
    print(string_combo + " , " + genHash(string_combo))

