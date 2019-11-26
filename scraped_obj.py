import requests
from bs4 import BeautifulSoup
import pandas as pd


class WIKIBook:
    """
    Class containing methods for parsing WIKI books websites from self.soup attribute.
    """

    def __init__(self, link, title):
        self.link = link
        self.title = title
        r = requests.get(link)
        r.encoding = 'UTF-8'
        self.soup = BeautifulSoup(r.text, 'html.parser')

        self.characteristics = self.parse_characteristics()

    def parse_characteristics(self):
        """
        Parses dictionary of values from the table into a pandas Series.
        :return: pandas series with WIKI_Book characteristics
        """
        table = self.get_all_th_rows()
        return pd.Series(table)

    def get_all_th_rows(self):
        """
        Finds table on the page of the selected book and parses its rows.
        :return: dict of 'row_name': 'row_value'
        """
        table = self.soup.find('tbody')
        rows = table.find_all('th', scope='row')
        rows_with_values = {**{'title': self.title},
                            **{row.text.strip(): row.next_sibling.text.strip() for row in rows}}
        return rows_with_values

