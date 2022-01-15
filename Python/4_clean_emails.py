from data_storage import connection
import pandas as pd


def clean_mail_text(corpus):

    new_corpus = []

    for i in range(len(corpus)):

        sentence = corpus[i].split()

        sentence = [x.replace("=C3=BC", "ü") for x in sentence]
        sentence = [x.replace("=C3=9F", "ß") for x in sentence]
        sentence = [x.replace("=C3=B6", "ö") for x in sentence]
        sentence = [x.replace("=C3=A4", "ä") for x in sentence]
        sentence = [x.replace("=C3=9C", "Ü") for x in sentence]
        sentence = [x.replace("=20", "") for x in sentence]

        
        for word in sentence:

            if "=" in word and sentence.index(word) != len(sentence) - 1:
                replace_string = sentence[sentence.index(word) + 1]
                sentence[sentence.index(word)] = word.replace("=", replace_string)
            
                del sentence[sentence.index(replace_string)]
    
            

        new_corpus.append(sentence)


    return new_corpus


df = pd.read_sql_query('''Select * from sot_stage1''', connection)

mail_text = df['text'].to_list()
new_mail_text = clean_mail_text(mail_text)

new_mail_text = [" ".join(x) for x in new_mail_text]
df['text'] = new_mail_text

# remove all mails with less than 15 words
df = df[df['text'].str.split().str.len() >= 15]

df.to_sql('sot_stage2', con=connection, if_exists="replace", index=False)




