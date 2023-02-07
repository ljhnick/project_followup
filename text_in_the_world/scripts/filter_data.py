import json
import pandas as pd

train_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/train.json'
val_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/train.json'

train = json.load(open(train_path))
val = json.load(open(val_path))

csv = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv_labeled_action/Actions.csv'

csv_data = pd.read_csv(csv)

action_columns = csv_data['Code']
action_columns.value_counts().plot(kind="barh")


print(train)