from bs4 import BeautifulSoup
import requests

def get_wikipedia_text(url: str):
    page = requests.get(url)
    yield page.status_code
    wikisoup = BeautifulSoup(page.content, 'html.parser')
    yield wikisoup.prettify() # for now, this will be changed to just text content later.


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Luke_Skywalker'
    status, content = get_wikipedia_text(url)
    print(status, content)