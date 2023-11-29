import pandas as pd
import sys
model = pd.read_csv('HTAN.model.csv')

errors = []

# Level 1 test

components =  model[model['DependsOn'].notna()][['Attribute','DependsOn']]

components['DependsOnList'] = components['DependsOn'].map(lambda x: x.split(','))
components['DependsOnList'] = components['DependsOnList'].map(lambda x: list(map(str.strip,x)))

attributes = model['Attribute'].to_list()

# Check for attributes that do not exist
for i, row in components.iterrows():
    dol = row['DependsOnList']
    for do in dol:
        if do in attributes:
            pass
        else:
            e = f'"{do}" used in component "{row["Attribute"]}" is not defined in the data model'
            errors.append(e)

if len(errors) == 0:
    pass
else:
    sys.exit("\n".join(errors))
