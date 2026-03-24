import requests, json, re
from bs4 import BeautifulSoup

urls = [
    'https://onlywhatsneeded.in/product/whey-isolate-500g',
    'https://onlywhatsneeded.in/product/plant-coffee-1kg',
    'https://onlywhatsneeded.in/product/whey-protein-2',
    'https://onlywhatsneeded.in/product/whey-coffee-1kg',
]

output = []
for url in urls:
    entry = {'url': url}
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    
    entry['has_next_data'] = bool(soup.find('script', id='__NEXT_DATA__'))
    entry['has_shopify'] = 'shopify' in r.text.lower()[:5000]
    
    # Check meta tags for price
    for meta in soup.find_all('meta'):
        name = meta.get('property', '') or meta.get('name', '')
        if 'price' in name.lower() or 'amount' in name.lower():
            entry[f'meta_{name}'] = meta.get('content')
    
    # Check JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            ld = json.loads(script.string)
            if isinstance(ld, dict) and 'offers' in ld:
                entry['jsonld_name'] = ld.get('name')
                entry['jsonld_offers'] = ld.get('offers')
        except: pass
    
    # Shopify .json
    handle = url.split('/')[-1]
    sr = requests.get(f'https://onlywhatsneeded.in/products/{handle}.json', headers={'User-Agent': 'Mozilla/5.0'})
    entry['shopify_json_status'] = sr.status_code
    if sr.status_code == 200:
        try:
            sd = sr.json()
            entry['shopify_product_title'] = sd.get('product', {}).get('title')
            variants = sd.get('product', {}).get('variants', [])
            entry['shopify_variants'] = [{'id': v['id'], 'title': v['title'], 'price': v['price'], 'grams': v.get('grams')} for v in variants[:3]]
        except: pass
    
    # Check for price patterns in script tags
    for script in soup.find_all('script'):
        text = script.string or ''
        if 'price' in text.lower() and ('product' in text.lower() or 'variant' in text.lower()) and len(text) > 100:
            idx = text.lower().find('price')
            entry['script_price_context'] = text[max(0,idx-80):idx+120]
            break
    
    output.append(entry)

with open('scraper/data/own_dump.json', 'w') as f:
    json.dump(output, f, indent=2)
print("Done. Check scraper/data/own_dump.json")
