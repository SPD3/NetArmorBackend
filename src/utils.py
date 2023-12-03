import string
from typing import List

def convert_strings_to_bools(strings: List[int]):
    for i in range(len(strings)):
        strings[i] = strings[i].lower() == "true"
    return strings
