from data_storage import connection
import pandas as pd
import os
os.system("pip install sklearn")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

############## Read Data #################
# read DataFrame
Corpus = pd.read_sql_query('''Select * from sot_stage5_encode_id''', connection)
Train_X = pd.read_sql_query('''Select * from X_train_id''', connection)
Test_X = pd.read_sql_query('''Select * from X_test_id''', connection)
Train_Y = pd.read_sql_query('''Select * from Y_train_id''', connection)
Test_Y = pd.read_sql_query('''Select * from Y_test_id''', connection)

# transform the df to array
Train_X = Train_X['text']
Test_X = Test_X['text']
Train_Y = Train_Y['Grund für Beschwerde']
Test_Y = Test_Y['Grund für Beschwerde']

############## Model Evaluation #################
from sklearn.metrics import f1_score

def evaluation(y_pred, y_true):
    """ This function evaluates the model calculating the weighted f1-score based
    on the inputs `y_pred` (predictions by the model) and `y_true` (actual values). 
    
    Parameters
    ----------
    y_pred: list or np.array
        This parameter stores the predicted classes.

    y_true: list or np.array
        This parameter stores the actual classes (true values).

    Returns
    -------
    This function returns weighted f1-score.
    """
    weighted_f1_score = f1_score(y_true, y_pred, average='weighted')
    
    return weighted_f1_score 

############## Word Vectorization #################
# build a vocabulary of words which it has learned from the corpus data
Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(Corpus['text'])

# assign a unique integer number to each of these words
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

############## ML Model Building #################
# Dummy Regressor
from sklearn.dummy import DummyClassifier
random_clf = DummyClassifier(strategy="uniform")
random_clf.fit(X, y)
# predict the labels on validation dataset
predictions_random_dummy = dummy_clf.predict(Train_X_Tfidf,Train_Y)
# Get f1 score
print("Dummy Random f1 Score -> ",evaluation(predictions_random_dummy, Test_Y)*100)