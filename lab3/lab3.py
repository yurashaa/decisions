import re
from condorcet import condorcet
from borda import borda

def open_file():
    return open("v7.txt")



file = open_file()
lines = []
benefits = []

for line in file:
    if (not (line and not line.isspace())): continue
    row = re.split(' ', re.sub('\n', '', line))
    new_benefits = re.split(',', row[1])
    for benefit in new_benefits:
        if benefit not in benefits: benefits.append(benefit)

    lines.append([row[0], new_benefits])

print("Дані:")
for line in lines: print(line)

print("\nМетод Кондорсе:")
condorcet_result = condorcet(lines, benefits)
print("Отже:", ">".join(condorcet_result["places"]))

print("\nМетод Борда:")
borda_result = borda(lines, benefits)
print("Підрахунки:")
for note in borda_result['note'].keys():
    print(note, ": ", borda_result["note"][note], " = ", borda_result["sum"][note])
print("Отже:", ">".join(condorcet_result["places"]))