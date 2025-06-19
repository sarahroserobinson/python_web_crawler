import requests, csv, json, datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser


class Crawl():

    def __init__(self, robot_url, start_url, max_depth, format):
        self.robot_url = robot_url
        self.start_url = start_url
        self.max_depth = max_depth
        self.format = format
    

    def run(self):
        rp = RobotFileParser()
        rp.set_url(self.robot_url)
        rp.read()
        visited_links = []
        urls_to_visit = [(self.start_url, 0)]
        while len(urls_to_visit) and len(visited_links) < 10:
            current_url, depth = urls_to_visit.pop(0)

            if depth > self.max_depth:
                break
        
            if self._check_if_already_visited(current_url, visited_links):
                continue

            if not self._ask_robots_permission(rp, current_url):
                print(f"Blocked by robots.txt: {current_url}")
                continue

            print(f"Visiting: {current_url}")

            try:
                res = requests.get(current_url)
                soup = BeautifulSoup(res.text, "html.parser")

                title_text = self._get_title(soup)
                visited_links.append((current_url, title_text))

                links = self._extract_links(soup, current_url)
                for link in links:
                    if link not in visited_links and link not in urls_to_visit:
                        urls_to_visit.append((link, depth + 1))
                        

            except Exception as e:
                print(f"Error fetching {current_url}: {e}")
    
        print("\nCrawler job complete. All links that were visited:")
        for link, title in visited_links:
            print(f"Visited URL: {link} \nTitle: {title}")
        
        self.export_as_file(visited_links)
        return visited_links


    def _ask_robots_permission(self, rp, url_to_crawl):
        return rp.can_fetch("*", url_to_crawl)
            
    def _get_title(self, soup):
        title = soup.find('title')
        title_text = ""
        if title:
            title_text = title.get_text() 
        else: 
            title_text = "No title"
        return title_text 


    def _check_if_already_visited(self, current_url, visited_links):
        return any(link == current_url for link in visited_links)

    def _extract_links(self, soup, current_url):
        links = []
        for url in soup.findAll('a'):
            href = url.get("href")
            if href and not href.startswith(("mailto:", "javascript:", "#")):
                full_url = urljoin(current_url, href)
                links.append(full_url)
        return links
    
    def create_filename(self):
        parsed_url = urlparse(self.start_url)
        domain = parsed_url.netloc.replace('.', '-')
        todays_date = datetime.datetime.now().date()
        filename = f"{domain}-{todays_date}.{self.format}"
        return filename
    
    def export_as_file(self, data):
        filename = self.create_filename()
        with open(filename, 'w') as file:
            if self.format == 'csv':
                writer = csv.writer(file)
                writer.writerows(data)
            elif self.format == 'json':
                json.dump(data, file)
            else:
                print("Unable to save to that format, please select either json or csv.")
        print(f"Data has been imported to a {self.format} file named {filename}")



crawler = Crawl(robot_url="https://developer.mozilla.org/robots.txt", start_url="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a", max_depth=3, format="csv")
crawler.run()


        
