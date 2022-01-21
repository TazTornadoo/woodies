from load_final_data import get_data

# id-encoded sets
X_train_id, X_test_id, y_train_id, y_test_id = get_data(encoding="id")
print(y_train_id.head())

# OHE-encoded sets
X_train_ohe, X_test_ohe, y_train_ohe, y_test_ohe = get_data(encoding="ohe")
print(y_train_ohe.head())