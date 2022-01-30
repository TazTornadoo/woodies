from data_storage import connection
import pandas as pd

# Down below you find a template to retrieve data in a dataframe and load it into a dataframe

df = pd.read_sql_query('''Write here your SQL query''', connection)
