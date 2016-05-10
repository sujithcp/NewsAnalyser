from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_only_text(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'lxml')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text

print(get_only_text('''http://www.ndtv.com/india-news/dont-jump-the-gun-nitish-kumar-on-party-leaders-son-wanted-for-murder-1404354'''))