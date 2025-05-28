import requests
from bs4 import BeautifulSoup

url = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a"
res = requests.get(url)


soup = BeautifulSoup(res.text, "html.parser")
for link in soup.findAll('a'):
    href = link.get("href")
    if href and href.startswith("https"):
        print(href)
