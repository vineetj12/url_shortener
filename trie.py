class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_url = False
        self.long_url = None  # Store the long URL when the short code ends here

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a short code with the associated long URL
    def insert(self, short_code, long_url):
        node = self.root
        for char in short_code:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_url = True
        node.long_url = long_url  # Store the long URL at the end of the short code

    # Search for a long URL given a short code
    def search(self, short_code):
        node = self.root
        for char in short_code:
            if char not in node.children:
                return None  
            node = node.children[char]
        if node.is_end_of_url:
            return node.long_url
        return None 