from data_storage import connection
import pandas as pd

# step 1: set threshold to filter out email lables with frequency under x percent
# step 2: transform email label into unique label-id; suitable for k-Nearest Neighbors, Decision Trees, Naive Bayes, Random Forest , Gradient Boosting, BERT... 

# read DataFrame
df = pd.read_sql_query('''Select * from sot_stage4''', connection)

# step 1
# set threshold in percentage (e.g. 3% out of all records)
thres = 3

# calculate the frequency of each email label
s = (df['Grund für Beschwerde'].value_counts(normalize=True) * 100).gt(thres)

# filter out those which do not reach pre-defined threshold
df = df.loc[df['Grund für Beschwerde'].isin(s[s].index)]

# step 2
# set model output as categorical and save it as new column label
df['GfB_label'] = pd.Categorical(df['Grund für Beschwerde'])

# transform output to numeric
df['Grund für Beschwerde'] = df['GfB_label'].cat.codes

df.to_sql('sot_stage5_encode_id', con=connection, if_exists="replace", index=False)
