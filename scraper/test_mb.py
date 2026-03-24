import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093?navKey=VRNT-165145"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"Status: {r.status_code}")

# Check JSON-LD
for s in soup.find_all('script', type='application/ld+json'):
    if s.string:
        try:
            data = json.loads(s.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                print("Price from LD-JSON:", data.get('offers', {}).get('price'))
        except Exception as e:
            pass

# Check NEXT_DATA
next_data = soup.find('script', id='__NEXT_DATA__')
if next_data and next_data.string:
    print('NEXT_DATA len:', len(next_data.string))
    prices = re.findall(r'"price"\s*:\s*(\d+)', next_data.string)
    if prices:
        print('Prices in NEXT_DATA (first 10):', prices[:10])
        
# Check direct DOM elements
price_div = soup.find(string=re.compile(r'₹'))
if price_div:
    print("Found ₹ in DOM:", price_div.parent.text.strip())
