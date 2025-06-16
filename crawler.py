import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser


def crawl(robot_url, url_to_crawl, max_depth):
    return check_links(robot_url, url_to_crawl, max_depth)


def ask_robots_permission(rp, url_to_crawl):
    return rp.can_fetch("*", url_to_crawl)
            

def check_links(robot_url, url, max_depth):
    rp = RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    visited_links = []
    urls_to_visit = [(url, 0)]
    while len(urls_to_visit) and len(visited_links) < 10:
        current_url, depth = urls_to_visit.pop(0)

        if depth > max_depth:
            break
        
        flag = False 
        for link, title in visited_links:
            if link == current_url:
                flag = True
                break
        
        if flag:
            continue

        if not ask_robots_permission(rp, current_url):
            print(f"Blocked by robots.txt: {current_url}")
            continue

        print(f"Visiting: {current_url}")

        try:
            res = requests.get(current_url)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.find('title')
            title_text = ""
            if title:
                title_text = title.get_text() 
            else: 
                title_text = "No title"
            visited_links.append((current_url, title_text))

            for url in soup.findAll('a'):
                href = url.get("href")
                if href and not href.startswith(("mailto:", "javascript:", "#")):
                    full_url = urljoin(current_url, href)
                    if full_url not in visited_links and full_url not in urls_to_visit:
                        urls_to_visit.append((full_url, depth + 1))
                        

        except Exception as e:
            print(f"Error fetching {current_url}: {e}")
    
    print("\nCrawler job complete. All links that were visited:")
    for link, title in visited_links:
        print(f"Visited URL: {link} \nTitle: {title}")
    
    return visited_links

print(crawl(robot_url="https://developer.mozilla.org/robots.txt", url_to_crawl="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a", max_depth=3))


        
        