
Search Engine Code

Author: Tsai, Hsiang-Mao
Date: 2023/11/25
Description:
This Python script implements a simple search engine using a Trie data structure. The search engine is designed to parse text from HTML webpages, build a Trie data structure with the parsed information, and allow users to search for specific words in the webpages.

TrieNode Class:

Represents a node in the Trie data structure.
Contains a dictionary for children nodes and another for page information.
insert_to_trie Function:

Inserts a word into the Trie, updating the page information.
search_in_trie Function:

Searches for a word in the Trie and returns page information if found.
parse_to_save Function:

Parses HTML webpages and cleans the text, removing specified characters and stop words.
Returns a list of unique cleaned text from all webpages.
build_search_engine Function:

Builds the search engine by creating a Trie from the parsed webpages.

main Function:
Reads stop words from the "stop_words.txt" file.
Parses webpages, builds the search engine, and enters a loop for user input.
Allows users to search for words in the webpages and displays results.

Algorithm:
1. The parse_to_save function iterates through each HTML file in the "webpages" folder.
2. It extracts text content using BeautifulSoup and converts it to lowercase for case-insensitive matching.
3. Special characters specified in the charDel list are removed from the text.
4. Stop words specified in the "stop_words.txt" file are also removed from the text.
5. The cleaned text from all webpages is stored in a list in descending order.

How to Run:
Execute the script using python search_engine.py in the command line.

Note:
The script uses BeautifulSoup for HTML parsing and a Trie data structure for efficient word lookup.
Stop words are used to filter out common words during the parsing process.