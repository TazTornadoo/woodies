from data_storage import connection
import pandas as pd
import os
os.system("pip install sklearn")
from sklearn.model_selection import train_test_split


# seed
seed = 0

# verbosity
verbose = True

############## for id-based encoded set #################
# read DataFrame
df_id = pd.read_sql_query('''Select * from sot_stage5_encode_id''', connection)

if verbose:
    # check distributions of class labels
    print("\nclasses are distributed like this:")
    print(df_id["GfB_label"].value_counts(normalize=True).round(2))

# splitting for the id-encoded set
X_train_id, X_test_id, y_train_id, y_test_id = train_test_split(df_id["text"],
                                                                df_id["Grund für Beschwerde"],
                                                                random_state=seed,
                                                                test_size=0.2,
                                                                stratify=df_id["Grund für Beschwerde"])

if verbose:
    # check splitting
    print("\ntrain set split this:")
    print(y_train_id.value_counts(normalize=True).round(2))
    print("\ntest set split this:")
    print(y_test_id.value_counts(normalize=True).round(2))

# save to database
X_train_id.to_sql('X_train_id', con=connection, if_exists="replace", index=False)
X_test_id.to_sql('X_test_id', con=connection, if_exists="replace", index=False)
y_train_id.to_sql('y_train_id', con=connection, if_exists="replace", index=False)
y_test_id.to_sql('y_test_id', con=connection, if_exists="replace", index=False)


############## for the one-hot-encoded set #################
df_ohe = pd.read_sql_query('''Select * from sot_stage5_encode_onehot''', connection)
# add auxiliary column to use for stratification
df_ohe['ohe_concat'] = df_ohe.iloc[:,1].astype(str) + df_ohe.iloc[:,2].astype(str) + df_ohe.iloc[:,3].astype(str)

if verbose:
    # check distributions of class labels
    print("\nclasses are distributed like this:")
    print(df_ohe["ohe_concat"].value_counts(normalize=True).round(2))

# splitting for the OHE-encoded set (using stratification from id-based (1 column) labelling)
X_train_ohe, X_test_ohe, y_train_ohe, y_test_ohe = train_test_split(df_ohe["text"],
                                                                    df_ohe["ohe_concat"],
                                                                    random_state = seed,
                                                                    test_size=0.2,
                                                                    stratify=df_ohe["ohe_concat"])

if verbose:
    # check splitting
    print("\ntrain set split this:")
    print(y_train_ohe.value_counts(normalize=True).round(2))
    print("\ntest set split this:")
    print(y_test_ohe.value_counts(normalize=True).round(2))                                                            
                                                            
# restore original OHE
# for training labels
y_train_ohe = pd.DataFrame(y_train_ohe)
y_train_ohe["GfB_Kulanz Beschädigung ohne Beleggrundlage"] = y_train_ohe.iloc[:,0].str[0]
y_train_ohe["GfB_Preisnachlass"] = y_train_ohe.iloc[:,0].str[1]
y_train_ohe["GfB_Verbuchung von Ressourcenartikel"] =  y_train_ohe.iloc[:,0].str[2] 
y_train_ohe= y_train_ohe.drop("ohe_concat", axis=1)
# for test labels
y_test_ohe = pd.DataFrame(y_test_ohe)
y_test_ohe["GfB_Kulanz Beschädigung ohne Beleggrundlage"] = y_test_ohe.iloc[:,0].str[0]
y_test_ohe["GfB_Preisnachlass"] = y_test_ohe.iloc[:,0].str[1]
y_test_ohe["GfB_Verbuchung von Ressourcenartikel"] =  y_test_ohe.iloc[:,0].str[2] 
y_test_ohe= y_test_ohe.drop("ohe_concat", axis=1)

# save to database
X_train_ohe.to_sql('X_train_ohe', con=connection, if_exists="replace", index=False)
X_test_ohe.to_sql('X_test_ohe', con=connection, if_exists="replace", index=False)
y_train_ohe.to_sql('y_train_ohe', con=connection, if_exists="replace", index=False)
y_test_ohe.to_sql('y_test_ohe', con=connection, if_exists="replace", index=False)