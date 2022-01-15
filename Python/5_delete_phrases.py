from data_storage import connection
import pandas as pd

# read DataFrame
df = pd.read_sql_query('''Select * from sot_stage2''', connection)

# hard-coded list of common German email phrases
phrases = ["sehr geehrte damen und herren", "damen und herren", "mit freundlichen grüßen", "hallo", "sehr geehrter herr", "sehr geehrte frau",
            "damen und herren", "mit freundlichen grüßen", "Diese Nachricht wurde von meinem Android Mobiltelefon mit WEB.DE Mail gesendet",
            "grüße", "guten tag", "guten abend", "sehr geehrtes", "kontaktformular holzprofi24 anrede: herr vorname:", "nachname:", "kontaktformular holzprofi24 anrede: frau vorname:"]

df_phrases = pd.DataFrame({'phrases': phrases})

# harmonize capitalization in order to allow matching
df_phrases['phrases'] = df_phrases.phrases.str.lower()
df['text'] = df.text.str.lower()

# remove phrases from emails
df['text'] = df.text.str.replace('|'.join(df_phrases.phrases), '')

# handle replies/forwards/...
# TODO
    
# remove all mails with less than 15 words
df = df[df['text'].str.split().str.len() >= 15]

df.to_sql('sot_stage3', con=connection, if_exists="replace", index=False)