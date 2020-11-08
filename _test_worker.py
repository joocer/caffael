"""

"""
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
import csv
from caffael.worker.baseworker import BaseWorker

def download_zip(url, savelocation, encoding='utf-8'):
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    for file in zipfile.namelist():
        for line in zipfile.open(file).readlines():
            yield line.decode(encoding="utf8")


class AcquireCWEWorker(BaseWorker):

    URL = r'https://cwe.mitre.org/data/csv/2000.csv.zip'

    def acquire(self, message):
        # the message is just a trigger, ignore the value of
        # message, and create a generator of the content of the
        # file we've downloaded
        data_reader = download_zip(self.URL, r'data/raw/2000-cwe.csv', 'iso-8859-1')

        headers = next(data_reader).split(",")
        for line in data_reader:
            values = line.split(",")
            zipped = dict(zip(headers, values))
            yield zipped

    def pre_validate(self, payload):
        for item in payload:
            try:
                return item.get('CWE-ID') != None
            except:
                return False
            return True

    def process(self, payload):
        return payload

    def post_validate(self, payload):
        return True


w = AcquireCWEWorker()
w.execute(None)