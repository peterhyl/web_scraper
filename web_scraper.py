import requests

from bs4 import BeautifulSoup
from collections import Counter


class Scraper:
    """
    Class to scraping URL and result property contain expected results
    """

    def __init__(self, url):
        self.url = url
        self.text = ''
        self.statistics = None
        self._scrap_url()

    @property
    def result(self):
        """
        Return the text and statistics into one dictionary
        """
        if self.text:
            return {'text': self.text, **self.statistics}
        else:
            return None

    def _get_statistics(self):
        """
        Collecting statistics such as words count, longest word and most common letter,
        statistic store into dictionary
        """
        if not self.text:
            raise AttributeError(f'Missing text from page: {self.url}')
        text = self.text.lower()
        word_list = text.split()
        counts = Counter(word_list).most_common()

        longest_word = max(word_list, key=len)

        best_letters = Counter(text)
        best_letter = ''
        for letter in best_letters.most_common():
            if letter[0].isalpha():
                best_letter = letter[0]
                break

        self.statistics = {'words_frequency': counts,
                           'longest_word': longest_word,
                           'best_letter': best_letter}

        self.text = self.text.replace('\n', '<br>')  # replace \n to <br> for HTML page

    def _scrap_url(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            html = requests.get(self.url)
            if not is_good_response(html):
                return
        except requests.RequestException as exp:
            print('Error during requests to {0} : {1}'.format(self.url, str(exp)))
            return

        soup = BeautifulSoup(html.content, 'html.parser')
        data = soup.findAll('p')
        texts = [element.get_text() for element in data]
        self.text = ''.join(texts)
        self._get_statistics()


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
