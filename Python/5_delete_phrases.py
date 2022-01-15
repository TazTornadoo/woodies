from data_storage import connection
import pandas as pd


def delete_phrases(sentences, phrases):

    return
    
df = pd.read_sql_query('''Select * from sot_stage2''', connection)
mail_text = df['text'].to_list()

df.to_sql('sot_stage3', con=connection, if_exists="replace", index=False)