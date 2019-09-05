import io
import requests
import zipfile

zip_file_url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"


def getAlexaTop1Million():
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('data/')

