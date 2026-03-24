import requests, json

urls = [
    'https://www.plixlife.com/product/super-strength-fermented-yeast-protein/1616/4435',
    'https://www.plixlife.com/product/plant-protein-powder/14',
    'https://www.plixlife.com/product/strength/31'
]

for url in urls:
    print(f"\n--- {url.split('/')[-2]} ---")
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    nd = soup.find('script', id='__NEXT_DATA__')
    if nd:
        data = json.loads(nd.string)
        product = data.get('props', {}).get('pageProps', {}).get('productPageData', {}).get('product', {})
        print(product.get('name'))
        for v in product.get('variants', [])[:3]:  # Print first 3
            print(f"  {v.get('sku')}: {v.get('name')}")
