import json

with open('scraper/data/plix_next_data.json', 'r') as f:
    data = json.load(f)

product = data.get('props', {}).get('pageProps', {}).get('productPageData', {}).get('product', {})
print(f"Product Name: {product.get('name')}")
print(f"Product ID: {product.get('id')}")
print(f"Slug: {product.get('slug')}")

variants = product.get('variants', [])
print(f"\nFound {len(variants)} variants:")
for i, v in enumerate(variants):
    print(f"\n--- Variant {i} ---")
    print(f"SKU: {v.get('sku')}")
    print(f"Name: {v.get('name')}")
    price = v.get('pricing', {}).get('price', {}).get('gross', {}).get('amount')
    print(f"Price: {price}")
    qty = v.get('quantityAvailable')
    print(f"Quantity Available: {qty}")
    
    # Attributes
    attrs = v.get('attributes', [])
    for a in attrs:
        attr_name = a.get('attribute', {}).get('name')
        attr_values = [val.get('name') for val in a.get('values', [])]
        print(f"  {attr_name}: {attr_values}")
