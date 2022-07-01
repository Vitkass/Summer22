import xml.etree.cElementTree as ET
import argparse
import os
from pathlib import Path

''' На вход прогамме в командной строке подается путь до директории, 
где располагаются файлы steup.py и xml файл с приставкой .robin-impinfo. Программа сравниваниет
номер версии в обоих файлах и выводит "Correct" если они сходятся, в противном случае выводится Error'''




def main():

    #tree = os.walk('Summer22/FileCopy')
    parser = argparse.ArgumentParser()
    parser.add_argument('tree_name', type=Path, help='Корневая директория проекта')
    args = parser.parse_args()
    tree = os.walk(args.tree_name)
    robin_path = setup_path = ''

    for main, dir, file in tree:
        for name in file:
            if '.robin-impinfo' in name:
                robin_path = main + '/' + name
            elif name == 'setup.py':
                setup_path = main + '/' + name
        
        if setup_path != '' and robin_path != '':
            break

    

    xml_file = ET.parse(robin_path)
    root = xml_file.getroot()
    keys = dict(root.attrib)

    robin_key = keys['version']
    setup_key = ''

    with open(setup_path, 'r') as f:
        for line in f:
            if 'version=' in line:
                setup_key = line.split('=')[1].strip('\n').strip(',').strip("'")
                break

    print("Correct" if robin_key == setup_key else "Error")




if __name__ == '__main__':
    exit(main())

