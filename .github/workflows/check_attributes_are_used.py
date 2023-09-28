import pandas as pd
import sys
model = pd.read_csv('HTAN.model.csv')

errors = []

# Level 1 test

components =  model[model['DependsOn'].notna()][['Attribute','DependsOn']]

components['DependsOnList'] = components['DependsOn'].map(lambda x: x.split(','))
components['DependsOnList'] = components['DependsOnList'].map(lambda x: list(map(str.strip,x)))

attributes = model['Attribute'].to_list()


# Check for attributes that are unused
all_dependson = components['DependsOnList'].to_list()
all_dependson = [item for sublist in all_dependson for item in sublist]
all_dependson = list(set(all_dependson))

all_validvalues = model[model['Valid Values'].notna()][['Valid Values']]
all_validvalues['Valid Values List'] = all_validvalues['Valid Values'].map(lambda x: x.split(','))
all_validvalues['Valid Values List'] = all_validvalues['Valid Values List'].map(lambda x: list(map(str.strip,x)))

all_validvalues = all_validvalues['Valid Values List'].to_list()
all_validvalues = [item for sublist in all_validvalues for item in sublist]
all_validvalues = list(set(all_validvalues))

all_uses = list(set(all_validvalues + all_dependson))

for att in attributes:
    if att in all_uses:
        pass
    elif att in components['Attribute'].tolist():
        pass
    elif att in ['Assay','Device','Sequencing','File','Publication']:
        pass
    else:
        e = f'"{att}" is is not used by any component'
        errors.append(e)

if len(errors) == 0:
    pass
else:
    sys.exit("\n".join(errors))
