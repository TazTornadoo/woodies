# Import packages for parsing the email txt files
from email.parser import BytesParser
from email.policy import default
from bs4 import BeautifulSoup
import unicodedata
import re

# Import packages for dealing with the data structures
import pandas as pd
import glob
from tqdm import tqdm


# Import the database connection
from data_storage import connection

# Get all paths for all .txt files
all_files = glob.glob("./Data/incoming@imail.sys/*/*.txt")

# Create different list objects
from_, to_, text, date = [], [], [], []

# The first thing to check is whether either
# headers["Topic-Thread"] == "Reklamation" or headers["X-iMailCategory"] == "Reklamation"
# whereas both have to be tried, because some mails do not have these keys

# Second thing which needs to be checked is, whether this is the first mail,
# viz. the original complaint or a follow up message
# if headers["In-Reply-To"]
# then then this email can be disregarded, because we only want the first emails

# Counter to check if not too many mails are unreadable
not_readable = 0

# For each file in the files
for mail in tqdm(all_files):
    # open the file and read the content
    with open(mail, 'rb') as fp:
        # Use the BytesParser to parse the different emails
        headers = BytesParser(policy=default).parse(fp)
    # Check if the email is in the right category
    if headers["Topic-Thread"] == "Reklamation" or headers["X-iMailCategory"] == "Reklamation":
        # Also check that is not a reply, but in fact the first one
        if not headers["In-Reply-To"]:
            # If that is the case, then try to extract all the wished data
            try:
                # Especially the text needs some preprocessing
                prep = unicodedata.normalize("NFKD", BeautifulSoup(headers.get_body(
                    preferencelist=('html', 'plain')).as_string(), 'html.parser').text)
                prep = prep.split("--- ORIGINAL MESSAGE BEGIN ---", 1)[1]
                prep = prep.split("--- ORIGINAL MESSAGE END ---", 1)[0]
                # Append the different extracted values to lists, which later on
                # will be combined to a dataframe.
                text.append(prep)
                to_.append(headers['to'])
                from_.append(headers['from'])
                date.append(headers["date"])
            # If any of the extractions should not have worked, increase the
            # not readable counter by one and continue with the next file
            except (AttributeError, IndexError) as e:
                not_readable += 1
                continue

# Assert that not too many files are not readable.
assert not_readable > 10

# create DataFrame
df = pd.DataFrame({"to": to_,
                   "from": from_,
                   "text": text,
                   "date": date})

# function to clean email addresses


def extract_mails(text):
    if "<" in text:
        pattern = r"(?<=<).*?(?=>)"
        return re.search(pattern, text).group(0)
    else:
        return text


# clean e-mail addresses column
df["from"] = df["from"].apply(extract_mails)


# Insert data to database
(df.to_sql('emails', con=connection, if_exists="replace", index=False))
