import pandas as pd
import re
model = pd.read_csv('HTAN.model.csv')

level1 =  model[model.Attribute.str.contains('Level 1$')][['Attribute','DependsOn']]

level1['DependsOnList'] = level1['DependsOn'].map(lambda x: x.split(','))
level1['DependsOnList'] = level1['DependsOnList'].map(lambda x: list(map(str.strip,x)))

l1_required = ['Component', 'Filename', 'File Format', 'HTAN Parent Biospecimen ID','HTAN Data File ID']

for req in l1_required:
    for i, row in level1.iterrows():
        if req in row['DependsOnList']:
            pass
        else:
            print(f'{req} is missing from DependsOn for attribute {row["Attribute"]}')
            print(row['DependsOnList'])

level234 =  model[model.Attribute.str.contains(r'Level [2|3|4]$')][['Attribute','DependsOn']]

level234['DependsOnList'] = level234['DependsOn'].map(lambda x: x.split(','))
level234['DependsOnList'] = level234['DependsOnList'].map(lambda x: list(map(str.strip,x)))

level234_required = ['Component', 'Filename', 'File Format', 'HTAN Parent Data File ID','HTAN Data File ID']

for req in level234_required:
    for i, row in level234.iterrows():
        if req in row['DependsOnList']:
            pass
        elif (row['Attribute'] in ['Imaging Level 2','SRRS Imaging Level 2']) and (req == 'HTAN Parent Data File ID'):
            #print(f'Skipping {req} as {row["Attribute"]} is one of Imaging Level 2 or SRRS Imaging Level 2')
            pass
        else:
            print(f'{req} is missing from DependsOn for attribute {row["Attribute"]}')