# Import generic wrappers^
import ktrain
from ktrain import text
from data_storage import connection

import pandas as pd

deleted_phrases = pd.read_sql("Select * from sot_stage3", connection)

thres = 8

# calculate the frequency of each email label
s = (deleted_phrases['Grund für Beschwerde'].value_counts(normalize=True) * 100).gt(thres)

# filter out those which do not reach pre-defined threshold
data = deleted_phrases.loc[deleted_phrases['Grund für Beschwerde'].isin(s[s].index)]

from sklearn import model_selection
train, test = model_selection.train_test_split(data, test_size=0.2, stratify = data["Grund für Beschwerde"])
train, validation = model_selection.train_test_split(train, test_size=0.2, stratify = train["Grund für Beschwerde"])

# Define the model repo
model_name = "bert-base-german-dbmdz-uncased"

# Download pytorch model
t = text.Transformer(model_name, maxlen=500,class_names=["0","1","2"])
trn = t.preprocess_train(train["text"].tolist(), train["Grund für Beschwerde"].tolist())
val = t.preprocess_test(validation["text"].tolist(), validation["Grund für Beschwerde"].tolist())

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data = val,batch_size=6)

learner.fit_onecycle(5e-5, 10)

predictor = ktrain.get_predictor(learner.model, preproc=t)
y_pred = predictor.predict(test["text"].tolist())

evaluation(y_pred, test["Grund für Beschwerde"].tolist())
