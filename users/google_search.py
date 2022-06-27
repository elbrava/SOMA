import json
from time import sleep

from googlesearch import search

d = {"love": "kill"}

for key in d.keys():
    query = key

    s = search("Google", num_results=100)
    print(s)
