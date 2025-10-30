total = 0
with open('/home/aikings/Documents/puzzle_output.txt', 'r') as fh:
    line = fh.readline()
    result = [x.strip() for x in line.split()]
    if len(result) == 2:
        num_1, num_2 = map(int, result)
        total += abs(num_1 - num_2)
print(total)
