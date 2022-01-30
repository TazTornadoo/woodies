from tqdm import tqdm
from spacy.lang.de.stop_words import STOP_WORDS
from spacy.tokens import Token
import de_core_news_sm
import spacy
from data_storage import connection
import pandas as pd
import os
os.system("pip install spacy -q")
os.system("python -m spacy download de_core_news_sm")


# IMPORTANT
# Before executing the python skript please execute the following line in the terminal
# python -m spacy download de_core_news_sm

def apply_spacy(list_of_list, list_of_stopwords):

    spacy_complaints = []

    print("applying tokenization")

    for complaint in tqdm(list_of_list):
        spacy_complaints.append(nlp(complaint))

    cleaned_corpus = []

    print('NLP preprocessing for mail texts')

    for sentence in tqdm(list_of_list):

        sentence_cleaned = [token.lower_ for token in nlp(sentence)
                            if token._.is_lemma_stop == False and
                            token.is_punct == False and
                            token.is_space == False and
                            token.is_alpha == True and
                            token.pos_ != "PROPN"]

        sentence_cleaned = [word for word in sentence_cleaned
                            if word not in list_of_stopwords]

        sentence_cleaned = ' '.join(sentence_cleaned)
        cleaned_corpus.append(sentence_cleaned)

    return cleaned_corpus


stopwords_collection = ['mit', 'freundlichen',
                        'grüßen', 'mfg', 'hallo',
                        'sehr', 'geehrter', 'geehrte', 'damen',
                        'herren', 'herr', 'diese', 'nachricht', 'gmx'
                        'mail', 'android', 'mobiltelefon',
                        'gesendet', 'dame', 're', 'aw']


def stop_words_getter(
    token): return token.text in STOP_WORDS or token.lemma_ in STOP_WORDS or token.is_lower in STOP_WORDS


Token.set_extension("is_lemma_stop", getter=stop_words_getter, force=True)


nlp = de_core_news_sm.load()
df = pd.read_sql_query('''Select * from sot_stage3''', connection)

complaint_text = df['text'].values.tolist()
complaint_text = apply_spacy(complaint_text, stopwords_collection)

df['text'] = complaint_text

df.to_sql('sot_stage4', con=connection, if_exists="replace", index=False)
