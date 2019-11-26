import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from scraped_obj import WIKIBook


class WIKIDownloader:
    def __init__(self, allow_log=True):
        self._allow_log = allow_log
        self.links = []
        self.books = []
        self.dfs = None
        if self._allow_log:
            print('Successfully initialized WIKI Books Downloader')

    def _get_links(self, soup):
        """
        find all neccessary links
        """
        links = [{'link': f"https://en.wikipedia.org{a['href']}",
                  'title': a['title']}
                 for a in soup.find('ol').find_all('a', href=True)]
        return links

    def get_books_links(self, link):
        """
        Downloads all books links in the specified webpage and saves it to self.links
        """
        if self._allow_log:
            print(f'Searching for Books-links of on {link} ...')
        r = requests.get(link)
        r.encoding = 'UTF-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        self.links = self._get_links(soup)

        if self._allow_log:
            print('Found {} Books-links'.format(len(self.links)))

    def download_books(self, pause=0.5):
        """
        Download all links stored in self.links and store it in self.books
        pause -- how long to pause between requests? (in seconds)
        """
        if self._allow_log:
            count = len(self.links)
            print(f'Downloading all {count} books ...')

        for book_info in self.links:
            book = WIKIBook(book_info['link'], book_info['title'])
            # print(book.characteristics)
            self.books.append(book)
            time.sleep(pause)
        if self._allow_log:
            print(f'Successfully downloaded {len(self.books)} books')

    def save_dfs(self):
        dfs = {
               'books': pd.DataFrame([x.characteristics for x in self.books])
        }
        self.dfs = dfs


if __name__ == '__main__':
    downloader = WIKIDownloader()
    downloader.get_books_links('https://en.wikipedia.org/wiki/20th_Century%27s_Greatest_Hits:_100_English-Language_Books_of_Fiction')
    downloader.download_books()
    downloader.save_dfs()
    print(downloader.dfs['books'].info())
