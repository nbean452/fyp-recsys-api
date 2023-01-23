import json
import os
import re
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import nltk

# regex = re.compile("[^-9A-Za-z ]")
regex = re.compile("[^\w\s]")

stopwords = nltk.corpus.stopwords.words('english')


def extract_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text()

    text_clean = regex.sub("", text).lower()
    words = nltk.tokenize.word_tokenize(text_clean)
    words_new = [i for i in words if i not in stopwords]
    wn = nltk.WordNetLemmatizer()
    words_clean = [wn.lemmatize(word) for word in words_new]
    text = ""
    for word in words_clean:
        text += " {}".format(word)

    return text


URL = "https://www.polyu.edu.hk/en/comp/study/subject-offerings_22_23/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find('table')

rows = []
for i, row in enumerate(table.find_all('tr')):
    if i != 0:
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
