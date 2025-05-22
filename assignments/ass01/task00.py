# Phonetic Encoding of Names

# (a) (1 point) Using your Python Soundex function, generate the Soundex codes for the
# following name strings: christina, kirstyn, allyson, alisen.

import sys 

sys.path.append("./")

from blocking.blocking_functions import soundex

names = ["christina", "kirstyn", "allyson", "alisen"]
names_soundex = {}
for name in names:
    names_soundex[name] = soundex(name=name)

print(names_soundex)