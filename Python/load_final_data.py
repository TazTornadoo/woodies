from data_storage import connection
import pandas as pd

# function to load the data for models
def get_data(encoding):
    """
    load the split data into dataframes

    args:
        encoding ([str]): "ohe" or "id"

    returns:
        X_train_<encoding>, X_test_encoding>, y_train_encoding>, y_test_encoding>
    """
    if encoding == "ohe":
        X_train_ohe = pd.read_sql_query('''Select * from X_train_ohe''', connection)
        X_test_ohe = pd.read_sql_query('''Select * from X_test_ohe''', connection)
        y_train_ohe = pd.read_sql_query('''Select * from y_train_ohe''', connection)
        y_test_ohe = pd.read_sql_query('''Select * from y_test_ohe''', connection)
        return X_train_ohe, X_test_ohe, y_train_ohe, y_test_ohe

    if encoding == "id":
        X_train_id = pd.read_sql_query('''Select * from X_train_id''', connection)
        X_test_id = pd.read_sql_query('''Select * from X_test_id''', connection)
        y_train_id = pd.read_sql_query('''Select * from y_train_id''', connection)
        y_test_id = pd.read_sql_query('''Select * from y_test_id''', connection)
        return X_train_id, X_test_id, y_train_id, y_test_id