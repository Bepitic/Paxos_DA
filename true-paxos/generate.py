#!/usr/bin/env python3
import random 

import sys

#a = random.sample(list(range(int(sys.argv[2]), int(sys.argv[3]))), int(sys.argv[1]), )
a = list(range(int(sys.argv[2]),int(sys.argv[2])+ int(sys.argv[1]) ))

print(sys.argv)
with open("../" + sys.argv[4], 'w') as f:
  # Iterate over the elements in the list
  for element in a:
    # Write each element to a new line in the file
    f.write(str(element) + '\n')