from email.parser import BytesParser, Parser
from email.policy import default
from bs4 import BeautifulSoup

import pandas as pd
import glob
from tqdm import tqdm
import unicodedata

all_files = glob.glob("./data/incoming@imail.sys/*/*.txt")

from_, to_, text, date = [], [], [], []

# The first thing to check is whether either
# headers["Topic-Thread"] == "Reklamation" or headers["X-iMailCategory"] == "Reklamation"
# whereas both have to be tried, because some mails do not have these keys

# Second thing which needs to be checked is, whether this is the first mail,
# viz. the original complaint or a follow up message
# if headers["In-Reply-To"]
# then then this email can be disregarded, because we only want the first emails

not_readable = 0
cntr = 0

glob.glob("./data/reklamation.csv")

for mail in tqdm(all_files):
    with open(mail, 'rb') as fp:
        headers = BytesParser(policy=default).parse(fp)

    if headers["Topic-Thread"] == "Reklamation" or headers["X-iMailCategory"] == "Reklamation":
        if not headers["In-Reply-To"]:
            try:
                prep = unicodedata.normalize("NFKD", BeautifulSoup(headers.get_body(preferencelist=('html', 'plain')).as_string(), 'html.parser').text)
                prep = prep.split("--- ORIGINAL MESSAGE BEGIN ---",1)[1]
                prep = prep.split("--- ORIGINAL MESSAGE END ---",1)[0] 
                text.append(prep)
                to_.append(headers['to'])
                from_.append(headers['from'])
                date.append(headers["date"])
            except (AttributeError, IndexError) as e:
                not_readable += 1
                continue

df = pd.DataFrame({"to": to_,
                            "from": from_,
                            "text": text,
                            "date": date})

df.to_csv("data/reklamation.csv")

print(not_readable)

#  Or for parsing headers in a string (this is an un
# common operation), use:
#headers = Parser(policy=default).parsestr(
#        'From: Foo Bar <user@example.com>\n'
#        'To: <someone_else@example.com>\n'
#        'Subject: Test message\n'
#        '\n'
#        'Body would go here\n')

#  Now the header items can be accessed as a dictionary:
print('To: {}'.format(headers['to']))
print('From: {}'.format(headers['from']))
print('Subject: {}'.format(headers['subject']))

# get body
body = headers.get_body(preferencelist=('html', 'plain'))


soup = BeautifulSoup(headers.get_body(preferencelist=('html', 'plain')).as_string(), 'html.parser')

dir(soup)

replaced_unicode = unicodedata.normalize("NFKD", BeautifulSoup(headers.get_body(preferencelist=('html', 'plain')).as_string(), 'html.parser').text) # payload has 7bit encoded data
import re
strings = re.sub(r"\n", "", replaced_unicode)
strings.encode("utf-8")

soup.get_text()
print(soup.prettify())

# You can also access the parts of the addresses:
print('Recipient username: {}'.format(headers['to'].addresses[0].username))
print('Sender name: {}'.format(headers['from'].addresses[0].display_name))