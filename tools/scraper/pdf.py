import requests
import os
import json


def download_pdf_file(url: str) -> bool:
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        # Save in pdfs folder
        filepath = os.path.join(
            os.getcwd(), 'tools/scraper/pdfs/'+pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False


BASE_URL = "https://www.polyu.edu.hk/comp/docdrive/ug/subject/"


# file will be run from the root folder!
f = open("base/batch_data/courses.json", "r")

contents_json = f.read()

f.close()

contents = json.loads(contents_json)

codes = set()

for content in contents:
    codes.add(content["fields"]["code"])

codes = list(codes)

for code in codes:
    URL = "{}{}.pdf".format(BASE_URL, code)
    download_pdf_file(URL)
