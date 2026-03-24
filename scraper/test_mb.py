import requests, json

# bgreen.in uses Shopify — the .json endpoint works!
sr = requests.get('https://bgreen.in/products/bgreen-plant-protein.json', headers={'User-Agent': 'Mozilla/5.0'})
data = sr.json()
product = data['product']

with open('scraper/data/bgreen_dump.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Title: {product['title']}")
print(f"Vendor: {product['vendor']}")

variants = product['variants']
print(f"\nVariants ({len(variants)}):")
for v in variants:
    print(f"  id={v['id']}")
    print(f"  title={v['title']}")
    print(f"  price=₹{v['price']}")
    print(f"  available={v.get('available')}")
    print(f"  grams={v.get('grams')}g")
    print(f"  sku={v.get('sku')}")
    print(f"  option1={v.get('option1')}")
    print(f"  option2={v.get('option2')}")
    print()

# Check body_html for nutritional info
body = product.get('body_html', '')
if 'protein' in body.lower():
    print("Body HTML has protein mentions")
    # Extract table data if any
    from bs4 import BeautifulSoup
    bsoup = BeautifulSoup(body, 'html.parser')
    tables = bsoup.find_all('table')
    print(f"Tables found: {len(tables)}")
    for t in tables:
        rows = t.find_all('tr')
        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if any('protein' in c.lower() or 'serving' in c.lower() for c in cells):
                print(f"  {cells}")
