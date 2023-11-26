import os
from bs4 import BeautifulSoup
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.page_info = defaultdict(int)

def insert_to_trie(root, word, page_name):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.page_info[page_name] += 1

def search_in_trie(root, word):
    node = root
    for char in word:
        if char not in node.children:
            return None
        node = node.children[char]
    return node.page_info

def parse_to_save(webpage_folder, stop_words):
    webpages = set()
    
    # Create list of characters to delete
    charDel = [".", ",", "/", "?", "<", ">", ":", ";", "[", "]", "{", "}", "-", "_", "+", "=", "|", '"', "!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

    


    for filename in os.listdir(webpage_folder):
        if not filename.endswith('.html') and not filename.endswith('.txt'):
            continue
        with open(os.path.join(webpage_folder, filename), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            text = soup.get_text().lower()
            
            for c in charDel:
                text = text.replace(c, ' ')

            for stop_word in stop_words:
                text = text.replace(stop_word, '')
            webpages.add(text)
    return list(webpages)

def build_search_engine(webpages):
    trie_root = TrieNode()


    for i, webpage in enumerate(webpages):
        for word in webpage.split():
            insert_to_trie(trie_root, word, i)

    return trie_root

def main():
    # webpage_folder = 'testpages'
    webpage_folder = 'webpages'
    stop_words_file = 'stop_words.txt'
    
    with open(stop_words_file, 'r', encoding='utf-8') as stop_words_file:
        stop_words = stop_words_file.read().split()

    webpages = parse_to_save(webpage_folder, stop_words)
    trie_root = build_search_engine(webpages)

    while True:
        search_term = input("Enter a word to search (or enter 'esc' to exit): ").lower()

        if search_term.lower() == 'esc':
            break

        result = search_in_trie(trie_root, search_term)

        if result is not None:
            # sort the result by frequency in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
            for page, frequency in result.items():
                print(f"Word '{search_term}' found in webpage: {page} with frequency: {frequency}")
        else:
            print(f"Word '{search_term}' not found in any webpages.")

if __name__ == "__main__":
    main()
