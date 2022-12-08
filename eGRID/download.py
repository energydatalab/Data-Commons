import sys
import os
import requests

_URL = "https://www.epa.gov/system/files/documents/2022-01/egrid2020_data.xlsx"
_RAW_PATH = 'raw_data'

current_dir = os.path.dirname(__file__)


def download_file(url, save_path):
    full_save_path = os.path.join(current_dir, save_path)
    if not os.path.exists(full_save_path):
        os.makedirs(full_save_path)  # create folder if it does not exist

        filename = url.split('/')[-1]
        file_path = os.path.join(full_save_path, filename)

        r = requests.get(url, stream=True)
        if r.ok:
            print(f'Downloading {url} and save to {full_save_path}')
            with open(file_path, 'wb') as f:
                f.write(r.content)
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(
                r.status_code, r.text))


def main():
    download_file(_URL, _RAW_PATH)


if __name__ == '__main__':
    main()
