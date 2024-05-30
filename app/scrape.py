from bs4 import BeautifulSoup
import requests

def get_wikipedia_text(url: str):
    page = requests.get(url)
    if page.status_code != 200:
        return Exception("Page couldn't be downloaded!")
    wikisoup = BeautifulSoup(page.content, 'html.parser')
    return wikisoup.find_all('p') # filter by class=mw-body-content?


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Luke_Skywalker'
    status, content = get_wikipedia_text(url)
    print(status, content)