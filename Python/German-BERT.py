# Import generic wrappers^
import ktrain
from ktrain import text
from load_final_data import get_data
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

# id-encoded sets
X_train_id, X_test_id, y_train_id, y_test_id = get_data(encoding="id")
print(y_train_id.head())


# Define the model repo
model_name = "bert-base-german-dbmdz-uncased" 


# Download pytorch model
t = text.Transformer(model_name, maxlen=500,class_names=["0","1","2"])
trn = t.preprocess_train(X_train_id["text"].tolist(), y_train_id["Grund für Beschwerde"].tolist())
val = t.preprocess_test(X_test_id["text"].tolist(), y_test_id["Grund für Beschwerde"].tolist())

model = t.get_classifier(metrics=["accuracy"])
learner = ktrain.get_learner(model, train_data=trn, val_data = val, batch_size=6)

learner.fit_onecycle(5e-5, 10)

learner.view_top_losses(n=5, preproc=t)

# We still have to do the accuracy