from data_storage import connection
import pandas as pd

# Down below you find a template to retrieve data in a dataframe and load it into a dataframe

df = pd.read_sql_query('''select a.text, d."Grund für Beschwerde" from 
                        (select * from emails z
                        group by z."from"
                        having count(*) = 1) a
                        join debitor_x_mail b on a."from" = b."E-Mail"
                        join sales c on b."Nr." = c."Sell-to Customer No_"
                        join complaint_codes d on c."Return Reason Code" = d.Reklamationscode''',
                       connection)

df = df.drop_duplicates(subset=['text'], keep='first')

df.to_sql('sot_stage1', con=connection, if_exists="replace", index=False)
