from data_storage import connection
import pandas as pd

# Read and input sales data to database
# If the database does not exist it will created automatically
(pd.read_csv("./Data/Source/HolzLandBecker$Sales Cr_ Memo Line.csv", dtype='str')
 .to_sql('sales', con=connection, if_exists="replace", index=False))

# Read and input the Reklamationscodes into the database
(pd.read_excel("./Data/Source/Reklamationsgrundcodes_Filter_v1.2.xlsm", dtype='str', header=16, index_col=0)
 .to_sql('complaint_codes', con=connection, if_exists="replace", index=False))

# Read file and input into the database.
(pd.read_excel("./Data/Source/Debitoren HOLZLANDBECKER_L.STUEBGEN 2021-12-13T16_42_31.xlsx", sheet_name="Debitoren", engine="openpyxl")
 .to_sql('debitor_x_mail', con=connection, if_exists="replace", index=False))
