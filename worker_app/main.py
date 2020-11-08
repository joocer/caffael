"""

"""
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from caffael.worker.baseworker import BaseWorker

def download_zip(url, savelocation, encoding='utf-8'):
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    for file in zipfile.namelist():
        for line in zipfile.open(file).readlines():
            yield line


class AcquireCWEWorker(BaseWorker):

    URL = r'https://cwe.mitre.org/data/csv/2000.csv.zip'

    def acquire(self, message):
        # the message is just a trigger, ignore the value of
        # message, and create a generator of the content of the
        # file we've downloaded
        return download_zip(self.URL, r'data/raw/2000-cwe.csv', 'iso-8859-1')

    def pre_validate(self, payload):
        for line in payload:
            print(line)


    def process(self, payload):
        return payload

    def post_validate(self, payload):
        return True


w = AcquireCWEWorker()
w.execute(None)