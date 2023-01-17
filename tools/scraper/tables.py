import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.polyu.edu.hk/en/comp/study/subject-offerings_22_23/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find('table')

header = []
rows = []
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])

arr = []


# print('header', header)
for index, row in enumerate(rows):
    availability = ""

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

    arr.append({
        "model": "base.Course",
        "fields": {
            "id": index + 1,
            "title": row[1],
            "code": row[0],
            "name": '{} {}'.format(row[0], row[1]),
            "description": "Empty description",
            "availability": availability,
            "is_active": True
        }
    })

print(json.dumps(arr))
