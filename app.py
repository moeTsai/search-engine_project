import os
from bs4 import BeautifulSoup
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.page_index = None

def insert_to_trie(root, word, page_index):
    node = root
    for char in word:
        if char not in node.children:    
            node.children[char] = TrieNode()
        node = node.children[char]
    node.page_index = page_index

def search_in_trie(root, word):
    node = root
    for char in word:
        if char not in node.children:
            return None
        node = node.children[char]
    return node.page_index

def print_trie_to_file(node, file, depth=0):
    if node.page_index is not None:
        file.write(" " * depth + str(node.page_index) + "\n")
    for char, child_node in node.children.items():
        print_trie_to_file(child_node, file, depth + 1)

            
def parse_to_save(webpage_folder, stop_words):
    webpages = set()

    for filename in os.listdir(webpage_folder):
        # open the file only if it is a .html file
        # print(os.listdir(webpage_folder))
        if not filename.endswith('.html'):
            continue
        with open(os.path.join(webpage_folder, filename), 'r', encoding='utf-8') as file:
            # print(filename)
            soup = BeautifulSoup(file.read(), 'html.parser')
            text = soup.get_text().lower()
            # print(text)
            for stop_word in stop_words:
                text = text.replace(stop_word, '')
            webpages.add(text)
    return list(webpages)

def build_search_engine(webpages, webpage_names):
    trie_root = TrieNode()
    
    for i, webpage in enumerate(webpages):
        for word in webpage.split():
            insert_to_trie(trie_root, word, i)

    return trie_root, webpage_names

def main():
    # webpage_folder = 'testpages'
    webpage_folder = 'webpages'
    stop_words_file = 'stop_words.txt'
    trie_output_file = 'trie_structure.txt'
    
    with open(stop_words_file, 'r', encoding='utf-8') as stop_words_file:
        stop_words = stop_words_file.read().split()

    webpage_names = []
    webpages = parse_to_save(webpage_folder, stop_words)

    print(webpages)

    for filename in os.listdir(webpage_folder):
        if not filename.endswith('.html'):
            continue
        webpage_names.append(filename)

    trie_root, webpage_names = build_search_engine(webpages, webpage_names)

    while True:
        search_term = input("Enter a word to search (or enter 'esc' to exit): ").lower()

        if search_term == 'esc':
            break

        result = search_in_trie(trie_root, search_term)

        if result is not None:
            print(f"Word '{search_term}' found in webpage: {webpage_names[result]}")
        else:
            print(f"Word '{search_term}' not found in any webpages.")

    print("Trie Structure:")
    with open(trie_output_file, 'w', encoding='utf-8') as trie_output:
        print_trie_to_file(trie_root, trie_output)

if __name__ == "__main__":
    main()
