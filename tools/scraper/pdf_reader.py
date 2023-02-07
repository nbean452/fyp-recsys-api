import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize
import string
from PyPDF2 import PdfReader

pdfs = [
    'COMP3211',
    'COMP1002',
    'COMP3235',
]


def extract_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        text += pdf.pages[0].extract_text()
        # for page in pdf.pages:
        #     text += page.extract_text()

    return text


prerequisite_regex = "COMP\d{4}"


for pdf in pdfs:
    text = extract_text('tools/scraper/pdfs/{}.pdf'.format(pdf))
    print("{}\n".format(json.dumps(text)))
    match = re.findall(prerequisite_regex, text)

    for code in match:
        if code == pdf:
            match.remove(code)

    print("{}\n".format(match))
