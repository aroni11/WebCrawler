import requests


def download_file(path):

    res = requests.get(path)
    if res.status_code == 200:
        return res.text
    else:
        res.raise_for_status()