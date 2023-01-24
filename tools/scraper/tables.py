import json
import os
import re
import string

import nltk
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from PyPDF2 import PdfReader

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


def normalize_text(paragraph):
    stopwords = set(nltk.corpus.stopwords.words('english'))

    # paragraph = """
    #         Lectures focus on introduction and explanation of key concepts and techniques.
    #         Tutorial/lab sessions provide students with opportunities to apply the theories and
    #         techniques in selected software engineering scenarios. Assignments, in-class
    #         exercises/quizzes, and the examination will be used to assess the students’
    #         understanding of the learned knowledge. The project requires the students to work
    #         in groups and apply the theories and techniques to solve problems in the development
    #         of serious software systems. Course's object.
    #         """

    slash_regex = re.compile("/")

    paragraph = slash_regex.sub(" ", paragraph)

    lemmatizer = WordNetLemmatizer()

    # Define function to lemmatize each word with its POS tag

    # POS_TAGGER_FUNCTION : TYPE 1

    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    original_words = word_tokenize(paragraph.lower())

    cleaned_words = []

    for word in original_words:
        if word not in stopwords and word not in string.punctuation and len(word) > 2:
            cleaned_words.append(word)
        else:
            continue

    # tokenize the sentence and find the POS tag for each token
    pos_tagged = nltk.pos_tag(cleaned_words)

    # print(pos_tagged)
    # # >[('the', 'DT'), ('cat', 'NN'), ('is', 'VBZ'), ('sitting', 'VBG'), ('with', 'IN'),
    # # ('the', 'DT'), ('bats', 'NNS'), ('on', 'IN'), ('the', 'DT'), ('striped', 'JJ'),
    # # ('mat', 'NN'), ('under', 'IN'), ('many', 'JJ'), ('flying', 'VBG'), ('geese', 'JJ')]

    # As you may have noticed, the above pos tags are a little confusing.

    # we use our own pos_tagger function to make things simpler to understand.
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    # print(wordnet_tagged)
    # # >[('the', None), ('cat', 'n'), ('is', 'v'), ('sitting', 'v'), ('with', None),
    # # ('the', None), ('bats', 'n'), ('on', None), ('the', None), ('striped', 'a'),
    # # ('mat', 'n'), ('under', None), ('many', 'a'), ('flying', 'v'), ('geese', 'a')]

    lemmatized_paragraph = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_paragraph.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_paragraph.append(lemmatizer.lemmatize(word, tag))
    lemmatized_paragraph = " ".join(lemmatized_paragraph)

    # print(lemmatized_paragraph)

    # print("sentences as a JSON file:\n{}".format(
    #     json.dumps(lemmatized_paragraph)))

    return lemmatized_paragraph


def extract_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text()

    return normalize_text(text)


URL = "https://www.polyu.edu.hk/en/comp/study/subject-offerings_22_23/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find('table')

rows = []
for index, row in enumerate(table.find_all('tr')):
    if index != 0:
        rows.append([el.text.strip() for el in row.find_all('td')])

arr = []


for index, row in enumerate(rows):
    availability = ""

    course = {
        "id": index + 1,
        "title": row[1],
        "code": row[0],
        "name": '{} {}'.format(row[0], row[1]),
        "is_active": True
    }

    if (row[2] == 'Yes'):
        availability += "A, "
    elif (row[2] == 'Day Class'):
        availability += "D, "
    elif (row[2] == 'Night Class'):
        availability += "N, "
    else:
        availability += "U, "

    if (row[3] == 'Yes'):
        availability += "A, "
    elif (row[3] == 'Day Class'):
        availability += "D, "
    elif (row[3] == 'Night Class'):
        availability += "N, "
    else:
        availability += "U, "

    if (row[4] == 'Yes'):
        availability += "A"
    elif (row[4] == 'Day Class'):
        availability += "D"
    elif (row[4] == 'Night Class'):
        availability += "N"
    else:
        availability += "U"

    course["availability"] = availability

    if "S" in course["code"]:
        continue

    if int(course["code"][4]) > 4:
        continue

    course["description"] = extract_text(
        'tools/scraper/pdfs/{}.pdf'.format(course["code"]))

    arr.append({
        "model": "base.Course",
        "fields": {
            "id": course["id"],
            "title": course["title"],
            "code": course["code"],
            "name": course["name"],
            "description": course["description"],
            "availability": course["availability"],
            "is_active": course["is_active"]
        }
    })

# print(json.dumps(arr))s


filepath = os.path.join(
    os.getcwd(), 'base/batch_data/courses.json')
with open(filepath, 'wb') as json_file:
    json_file.write(str.encode(json.dumps(arr)))
    print('courses.json was successfully saved!')
