alive_cells = {
    (0, 1), (0, 2), (1, 8), (3, 2)
}

sparse = {
    
}

for (x, y) in alive_cells:
    if (x , y) not in sparse:
        print("Adding new sp alive element")
        sparse[(x, y)] = 0

for (x, y) in alive_cells:
    for i in range(-1, 2):
            for j in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                if (i + x, j + y) in sparse:
                    sparse[(i+x, j+y)] += 1
                    print("increment")
                else:
                    sparse[(i+x, j+y)] = 1
                    print("Adding new sp element")
        

print(sparse)