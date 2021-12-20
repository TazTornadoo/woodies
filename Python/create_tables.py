from data_storage import create_connection, connection
import pandas as pd
import os

sales = pd.read_csv("./Data/Source/HolzLandBecker$Sales Cr_ Memo Line.csv", dtype='str')
complaint_codes = pd.read_csv("./Data/Source/complaint_codes.csv", dtype='str', encoding="utf_8", encoding_errors = 'ignore')
debitor_x_mail = pd.read_excel("./Data/Source/Debitoren HOLZLANDBECKER_L.STUEBGEN 2021-12-13T16_42_31.xlsx", sheet_name= "Debitoren", engine = "openpyxl")

sales.to_sql('sales', con=connection, if_exists="replace", index=False)
complaint_codes.to_sql('complaint_codes', con=connection, if_exists="replace", index=False)
debitor_x_mail.to_sql('debitor_x_mail', con=connection, if_exists="replace", index=False)



