import requests
from bs4 import BeautifulSoup

url = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a"
res = requests.get(url)


soup = BeautifulSoup(res.text, "html.parser")

def find_absolute_and_relative_links():
    for link in soup.findAll('a'):
        href = link.get("href")
        if href:
            if href.startswith("http"):
                print(f"Absolute: {href}")
            else:
                print(f"Relative: {href}")


visited_links = set()
urls_to_visit = ["https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a"]
while len(urls_to_visit) >= 1:
    current_url = urls_to_visit.pop(0)
    if current_url not in visited_links:
        print(f"Visiting: {current_url}")
        


    
        
        