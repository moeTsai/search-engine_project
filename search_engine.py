# Author: Tsai, Hsiang-Mao
# date: 2023/11/25

import os
from bs4 import BeautifulSoup
from collections import defaultdict

class TrieNode:
    """
    Trie node class.
    """
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.page_info = defaultdict(int)

def insert_to_trie(root, word, page_name):
    """
    Insert a word into the trie.
    """
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]

    # Increment the frequency of the word in the page
    node.page_info[page_name] += 1

def search_in_trie(root, word):
    """
    Search for a word in the trie.
    """
    node = root
    for char in word:
        # If the character is not in the trie, return None
        if char not in node.children:
            return None
        node = node.children[char]
    return node.page_info

def parse_to_save(webpage_folder, stop_words):
    """
    Parse the webpages and save the text in a list.
    """
    webpages = set()
    
    # Create list of characters to delete
    charDel = [".", ",", "/", "?", "<", ">", ":", ";", "[", "]", "{", "}", "-", "_", "+", "=", "|", '"', "!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

    for filename in os.listdir(webpage_folder):
        # Skip non-html and non-text files
        if not filename.endswith('.html') and not filename.endswith('.txt'):
            continue
        with open(os.path.join(webpage_folder, filename), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            text = soup.get_text().lower()
            
            for c in charDel:
                text = text.replace(c, ' ')

            for stop_word in stop_words:
                text = text.replace(stop_word, '')
            
            # print(text)
            webpages.add(text)
    return list(webpages)

def build_search_engine(webpages):
    """
    build the search engine.
    """
    trie_root = TrieNode()

    # Insert each word in each webpage into the trie
    for i, webpage in enumerate(webpages):
        for word in webpage.split():
            insert_to_trie(trie_root, word, i)

    return trie_root

def main():
    """
    Main function.
    """
    webpage_folder = 'webpages'
    stop_words_file = 'stop_words.txt'
    
    # Read stop words from file
    with open(stop_words_file, 'r', encoding='utf-8') as stop_words_file:
        stop_words = stop_words_file.read().split()

    # Parse the webpages and save the text in a list
    webpages = parse_to_save(webpage_folder, stop_words)
    trie_root = build_search_engine(webpages)

    while True:
        search_term = input("Enter a word to search (or enter 'esc' to exit): ").lower()
        # Exit the program if the user enters 'esc'
        if search_term.lower() == 'esc':
            break

        # Search for the word in the trie
        result = search_in_trie(trie_root, search_term)

        if result is not None:
            # sort the result by frequency in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

            # Print the result
            for page, frequency in result.items():
                print(f"Word '{search_term}' found in webpage: {page} with frequency: {frequency}")
        else:
            print(f"Word '{search_term}' not found in any webpages.")

if __name__ == "__main__":
    main()
