import requests
from bs4 import BeautifulSoup

url = "https://example.com"
res = requests.get(url)


soup = BeautifulSoup(res.text, "html.parser")
print(soup)
for link in soup.findAll('a'):
    print(link)
