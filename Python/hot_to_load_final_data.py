from load_final_data import get_data

X_train_id, X_test_id, y_train_id, y_test_id = get_data(encoding="id")

print(X_train_id.head())