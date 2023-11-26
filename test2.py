import re
import requests
from bs4 import BeautifulSoup

class SearchEngine:
    def __init__(self):
        self.stop_words = self.load_stop_words()
        self.trie = {}
        self.page_index = {}

    def load_stop_words(self):
        with open('stop_words.txt', 'r') as f:
            stop_words = f.read().split(',')
        return set(stop_words)

    def parse_webpage(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            # Remove HTML tags and punctuation
            text = re.sub(r'<.*?>', '', text)
            text = re.sub(r'[^\w\s]', '', text)

            # Convert text to lowercase and split into words
            words = text.lower().split()

            # Remove stop words
            words = [word for word in words if word not in self.stop_words]

            # Add words to trie
            for word in words:
                self.add_word_to_trie(word, url)

        except Exception as e:
            print(f'Error parsing webpage: {e}')

    def add_word_to_trie(self, word, url):
        if word not in self.trie:
            self.trie[word] = {}

        node = self.trie[word]
        for char in word:
            if char not in node:
                node[char] = {}

            node = node[char]

        if 'docs' not in node:
            node['docs'] = []

        node['docs'].append(url)

    def search(self, query):
        words = query.lower().split()
        results = []

        for word in words:
            if word not in self.trie:
                continue

            node = self.trie[word]
            docs = node['docs']

            # Rank results based on word frequency
            ranked_docs = []
            for doc in docs:
                word_frequency = self.count_word_frequency(doc, word)
                ranked_docs.append((doc, word_frequency))

            ranked_docs.sort(key=lambda doc: doc[1], reverse=True)
            results += [doc for doc, _ in ranked_docs]

        return results

    def count_word_frequency(self, url, word):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        # Count the number of occurrences of the word in the text
        word_count = 0
        for match in re.finditer(r'\b{}\b'.format(word), text):
            word_count += 1

        return word_count

def main():
    search_engine = SearchEngine()

    # Parse webpages
    with open('webpage/webpage1.txt', 'r') as f:
        for url in f:
            search_engine.parse_webpage(url.strip())

    while True:
        query = input('Enter a search query: ')
        if query == '':
            break

        results = search_engine.search(query)
        if results:
            print('Results:')
            for url in results:
                print(f' - {url}')
        else:
            print('No results found')

if __name__ == '__main__':
    main()
