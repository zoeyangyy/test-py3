import requests
from bs4 import BeautifulSoup

r = requests.get('')
soup = BeautifulSoup(r.text)


