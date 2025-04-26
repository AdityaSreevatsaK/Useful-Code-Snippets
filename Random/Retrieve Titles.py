file_path = '../README.md'

with open(file_path, 'r') as file:
    lines = file.readlines()

titles = [line.strip().strip('###') for line in lines if line.strip().startswith('###')]

for title in titles:
    print(title)
