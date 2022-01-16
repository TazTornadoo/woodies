from data_storage import connection
import pandas as pd

# transform email label into unique label-id; suitable for k-Nearest Neighbors, Decision Trees, Naive Bayes, Random Forest , Gradient Boosting, BERT... 

# read DataFrame
df = pd.read_sql_query('''Select * from sot_stage4''', connection)

# set model output as categorical and save it as new column label
df['GfB_label'] = pd.Categorical(df['Grund für Beschwerde'])

# transform output to numeric
df['Grund für Beschwerde'] = df['GfB_label'].cat.codes

df.to_sql('sot_stage5_encode_id', con=connection, if_exists="replace", index=False)
