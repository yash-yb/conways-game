alive_cells = {
    (0, 1), (0, 2), (1, 8), (3, 2)
}

sparse = {}
for (x, y) in alive_cells:
    for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (i + x, j + y) in sparse:
                    sparse[(i+x, j+y)] += 1
                    print("increment")
                else:
                    sparse[(i+x, j+y)] = 1
                    print("Adding new sp element")
        
new_alive_cells = set()

for (x, y) in sparse:
    if (x, y) in alive_cells:
        if sparse[(x, y)] == 2 or sparse[(x, y)] == 3:
            new_alive_cells.add((x, y))
    elif sparse[(x, y)] == 3:
        new_alive_cells.add((x, y))

print(new_alive_cells)