import random

# Read lines from the input file
with open("templines.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Shuffle the lines
random.shuffle(lines)

# Write shuffled lines to the output file
with open("templines.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
