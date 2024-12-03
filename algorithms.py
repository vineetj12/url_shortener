# algorithms.py

import heapq

# Greedy Algorithm for URL Shortening
def greedy_shortener(url_list, access_frequencies):
    url_list.sort(key=lambda url: access_frequencies[url], reverse=True)
    shortened_urls = {}
    for url in url_list:
        code = generate_short_code(url)
        shortened_urls[url] = code
    return shortened_urls

# Priority Queue (Min-Heap) Algorithm
def priority_queue_shortener(url_list, access_frequencies):
    min_heap = []
    for url in url_list:
        heapq.heappush(min_heap, (access_frequencies[url], url))

    optimized_urls = {}
    while min_heap:
        frequency, url = heapq.heappop(min_heap)
        optimized_urls[url] = generate_short_code(url)

    return optimized_urls

# Generate short code for each URL
def generate_short_code(url):
    return url[:6] 

# Huffman Coding Algorithm
class Node:
    def __init__(self, url, frequency):
        self.url = url
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def huffman_encoding(url_list, access_frequencies):
    heap = [Node(url, access_frequencies[url]) for url in url_list]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.url + right.url, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    huffman_codes = {}
    def generate_codes(node, current_code=""):
        if node is not None:
            if not node.left and not node.right:
                huffman_codes[node.url] = current_code
            generate_codes(node.left, current_code + "0")
            generate_codes(node.right, current_code + "1")

    root = heap[0]
    generate_codes(root)
    return huffman_codes