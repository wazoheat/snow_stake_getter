import pathlib
import requests
import yaml

from bs4 import BeautifulSoup

conf = yaml.safe_load(pathlib.Path('stakes.yml').read_text())

for entry in conf:
    r = requests.get(conf[entry]["url"])
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    print(soup.prettify())

