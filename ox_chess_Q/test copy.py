import json
from collections import defaultdict

d = defaultdict(int)
d[("hello", 2)] = 5
print(d[("hello2", 3)])