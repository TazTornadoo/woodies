from data_storage import connection
import pandas as pd

# onehot encode email label; suitable for Logistic Regression, Support Vector Machine, LSTM ... 

# read DataFrame
df = pd.read_sql_query('''Select * from sot_stage4''', connection)

# onehot encode email lable
df = pd.get_dummies(df, prefix = "GfB", columns = ['Grund für Beschwerde'])

df.to_sql('sot_stage5_encode_onehot', con=connection, if_exists="replace", index=False)