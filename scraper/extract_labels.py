"""Extract incomplete products and their label images, write results to a file."""
import requests, json, re
from bs4 import BeautifulSoup

def get_label_images(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    nd = soup.find('script', id='__NEXT_DATA__')
    data = json.loads(nd.string)
    res = data['props']['pageProps']['data']['results']
    page = res.get('page', {})
    images = []
    for sec in page.get('pgSections', []):
        for item in sec.get('scContent', []):
            dis_nm = item.get('dis_nm', '')
            for attr in item.get('attributeArea', []):
                value = attr.get('value', '')
                if isinstance(value, str) and '<img' in value:
                    img_soup = BeautifulSoup(value, 'html.parser')
                    for img in img_soup.find_all('img'):
                        src = img.get('src', '')
                        if src:
                            images.append({'section': dis_nm, 'url': src})
    return images

brands = json.load(open('scraper/data/brands.json'))
catalog = json.load(open('public/master_catalog.json'))
cat_lookup = {p['id']: p for p in catalog}

output = []
for brand in brands:
    for product in brand['products']:
        pid = product['product_id']
        cat = cat_lookup.get(pid, {})
        missing = []
        if cat.get('serving_size_g') is None: missing.append('serving_size')
        if cat.get('protein_per_serving_g') is None: missing.append('protein_per_serving')
        if cat.get('num_servings') is None: missing.append('num_servings')
        
        if missing:
            imgs = get_label_images(product['url'])
            output.append({
                'product_id': pid,
                'name': cat.get('product_name', product['name']),
                'brand': brand['brand_id'],
                'missing_fields': missing,
                'has_protein_pct': cat.get('protein_claimed_percent'),
                'has_price': cat.get('live_price_inr'),
                'label_images': [i['url'] for i in imgs],
            })

with open('scraper/data/incomplete_products.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Found {len(output)} products with missing nutritional data.")
for item in output:
    print(f"\n[{item['brand']}] {item['name'][:60]}")
    print(f"  Missing: {', '.join(item['missing_fields'])}")
    print(f"  Has protein%: {item['has_protein_pct']}, price: {item['has_price']}")
    print(f"  Label images: {len(item['label_images'])}")
    for img in item['label_images'][:2]:
        print(f"    {img}")
