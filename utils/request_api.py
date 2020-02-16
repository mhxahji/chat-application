import csv
import requests

from utils.constants import API_URL


def get_csv_response_api(param):
    with requests.Session() as s:
        download = s.get(API_URL % param)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        return list(cr)
