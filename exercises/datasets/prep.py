

with open('exercises/datasets/images.csv','r') as f:
    lines = f.readlines()
    for line in lines:
        newline = line.replace('"', '')
        print(newline)