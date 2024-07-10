import sys
from utils.chords import keys, chords
from utils.specialprint import printe, filecolored

if sys.argv[1] in ["-h", "--help"]:
    print("find the chord name from its notes")
    print("example usage: 'python chord_finder.py c d# g'")
    exit()

input_keys = []
for i in sys.argv[1:]:
    key = i.lower()
    if key not in [x[0] for x in keys]:
        printe(f"{key}: invalid key")
    input_keys.append(key)

numbers = []
for x in input_keys:
    for key in keys:
        if x == key[0]:
            numbers.append(key[1])
numbers.sort()

for i in range(1, 13):
    numbers2 = []
    for n in numbers:
        while n + i > 12:
            n -= 12
        numbers2.append(n + i)
        numbers2.sort()
    for x in chords:
        if numbers2 == x[1]:
            chord = x[0]
            print(filecolored(keys[12 - i][0].upper()) + chord)
