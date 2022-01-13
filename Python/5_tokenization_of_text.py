from data_storage import connection
import pandas as pd
import spacy
import de_core_news_sm
from spacy.tokens import Token
from spacy.lang.de.stop_words import STOP_WORDS


# IMPORTANT 
# Before executing the python skript please execute the following line in the terminal
# python -m spacy download de_core_news_sm

def apply_spacy(list_of_list):

    spacy_complaints = []

    for complaint in list_of_list:
        spacy_complaints.append(nlp(complaint))

    
    cleaned_corpus = []


    for sentence in list_of_list:

        sentence_cleaned = [token.lower_ for token in nlp(sentence)
                            if token._.is_lemma_stop == False and 
                            token.is_punct == False and 
                            token.is_space == False and
                            token.is_alpha == True]
        
        cleaned_corpus.append(sentence_cleaned)


    return cleaned_corpus

stop_words_getter = lambda token: token.text in STOP_WORDS or token.lemma_ in STOP_WORDS or token.is_lower in STOP_WORDS 
Token.set_extension("is_lemma_stop", getter=stop_words_getter, force=True)


nlp = de_core_news_sm.load()

df = pd.read_sql_query('''Select * from sot_stage2''', connection)

complaint_text = df['text'].values.tolist()

complaint_text = apply_spacy(complaint_text)

print(complaint_text[234])