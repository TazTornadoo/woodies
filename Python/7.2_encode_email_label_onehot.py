from data_storage import connection
import pandas as pd

# step 1: set threshold to filter out email lables with frequency under x percent
# step 2: onehot encode email label; suitable for Logistic Regression, Support Vector Machine, LSTM ...

# read DataFrame
df = pd.read_sql_query('''Select * from sot_stage4''', connection)

# step 1
# set threshold in percentage (e.g. 3% out of all records)
thres = 8

# calculate the frequency of each email label
s = (df['Grund für Beschwerde'].value_counts(normalize=True) * 100).gt(thres)

# filter out those which do not reach pre-defined threshold
df = df.loc[df['Grund für Beschwerde'].isin(s[s].index)]

# step 2
# onehot encode email lable
df = pd.get_dummies(df, prefix="GfB", columns=['Grund für Beschwerde'])

df.to_sql('sot_stage5_encode_onehot', con=connection,
          if_exists="replace", index=False)
