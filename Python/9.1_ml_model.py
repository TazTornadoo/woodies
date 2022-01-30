from sklearn.metrics import f1_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection, naive_bayes, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from data_storage import connection
import pandas as pd
import os
os.system("pip install sklearn")

############## Read Data #################
# read DataFrame
Corpus = pd.read_sql_query(
    '''Select * from sot_stage5_encode_id''', connection)
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
# Classifier - Algorithm - Naive Bayes
# fit the training dataset on the NB classifier
Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_X_Tfidf, Train_Y)
# predict the labels on validation dataset
predictions_NB = Naive.predict(Test_X_Tfidf)
# Get the accuracy & f1 score
print("Naive Bayes Accuracy Score -> ",
      accuracy_score(predictions_NB, Test_Y)*100)
print("Naive Bayes f1 Score -> ", evaluation(predictions_NB, Test_Y)*100)

# Classifier - Algorithm - SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=100, kernel='rbf', gamma=0.01, decision_function_shape='ovr')
SVM.fit(Train_X_Tfidf, Train_Y)
# predict the labels on validation dataset
predictions_SVM = SVM.predict(Test_X_Tfidf)
# Get the accuracy & f1 score
print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, Test_Y)*100)
print("SVM f1 Score -> ", evaluation(predictions_SVM, Test_Y)*100)

# Classifier - Algorithm - RandomForest
# fit the training dataset on the classifier
RF = RandomForestClassifier(
    n_estimators=20, criterion='entropy', random_state=42)
RF.fit(Train_X_Tfidf, Train_Y)
# predict the labels on validation dataset
predictions_RF = RF.predict(Test_X_Tfidf)
# Get the accuracy & f1 score
print("RF Accuracy Score -> ", accuracy_score(predictions_RF, Test_Y)*100)
print("RF f1 Score -> ", evaluation(predictions_RF, Test_Y)*100)

############## Gridsearch for SVM #################
# defining parameter range
# param_grid = {'C': [0.1, 1, 10, 100, 1000],
#              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
#              'kernel': ['rbf', 'linear', 'sigmoid']}

#grid = GridSearchCV(svm.SVC(), param_grid, refit = True, verbose = 3)

# fitting the model for grid search
#grid.fit(Train_X_Tfidf, Train_Y)

# print best parameter after tuning
# print(grid.best_params_)
