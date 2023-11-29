import pandas as pd
import sys
model = pd.read_csv('HTAN.model.csv')

errors = []

# Level 1 test

components =  model[model['DependsOn'].notna()][['Attribute','DependsOn']]

components['DependsOnList'] = components['DependsOn'].map(lambda x: x.split(','))
components['DependsOnList'] = components['DependsOnList'].map(lambda x: list(map(str.strip,x)))

attributes = model['Attribute'].to_list()

# Check for attributes that exist more than once
for att in attributes:
    count = attributes.count(att)
    if count == 1:
        pass
    else:
        e = f'"{att}" appears {count} times in the data model'
        errors.append(e)

# check that DependsOn entries are unique
for i, row in components.iterrows():
    dol = row['DependsOnList']
    repeated_values = [x for x in set(dol) if dol.count(x) > 1]
    if len(repeated_values) == 0:
        pass
    else:
        e = f'"{row["Attribute"]}" has duplicate entries in DependsOn: {repeated_values}'
        errors.append(e)


if len(errors) == 0:
    pass
else:
    sys.exit("\n".join(errors))
