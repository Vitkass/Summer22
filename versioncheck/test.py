import os

tree = os.walk('Summer22/FileCopy')

robin_path = setup_path = ''

for main, dir, file in tree:
    for name in file:
        if '.robin-impinfo' in name:
            robin_path = main + '/' + name
        elif name == 'setup.py':
            setup_path = main + '/' + name
    
    if setup_path != '' and robin_path != '':
        break
        

with open(setup_path, 'r') as f:
    for line in f:
        if 'version=' in line:
            setup_key = line.split('=')[1].strip('\n').strip(',').strip("'")
            break


print(robin_path, setup_path, sep='\n')