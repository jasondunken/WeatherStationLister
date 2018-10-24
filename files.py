from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def get_data(source_url):
    html_page = urlopen(source_url)
    soup = BeautifulSoup(html_page, features="html.parser")
    links = []
    link_count = 0
    for link in soup.findAll('a', attrs={'href': re.compile("^")}):
        link = link.get('href')
        if link.startswith("/"):
            if ';' in link:
                if link.partition(';') and link.partition(';')[0].endswith('txt'):
                    links.append(source_url + link[5:])
                    link_count += 1
    print("%s links found @%s" % (link_count, source_url))
    return links
