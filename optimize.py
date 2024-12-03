import hashlib
import base64  # Import base64 module to avoid NameError

def optimize_codes(url_list, access_frequencies):
    # Sort URLs by their access frequency (higher frequency gets shorter code)
    sorted_urls = sorted(url_list, key=lambda url: access_frequencies[url], reverse=True)
    
    # Generate short codes for each URL
    code_assignment = {}
    total_length = 0

    # Assign shorter codes to more frequent URLs
    for idx, url in enumerate(sorted_urls):
        # create a short code based on the URL's index in the sorted list
        short_code = generate_short_code(url)
        code_assignment[url] = short_code
        total_length += len(short_code)

    return code_assignment, total_length

# Function to generate a short code (simplified for this example)
def generate_short_code(long_url):
    return base64.urlsafe_b64encode(hashlib.md5(long_url.encode()).digest()[:6]).decode('utf-8')
