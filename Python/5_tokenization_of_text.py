from data_storage import connection
import pandas as pd
import spacy

df = pd.read_sql_query('''Select * from sot_stage2''', connection)