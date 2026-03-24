import json
data = json.load(open('public/master_catalog.json'))
for p in data:
    w = p.get('total_weight_g')
    name = p['product_name'][:65]
    stock = p.get('in_stock')
    print(f"{name:65s} | {w}g | stock={stock}")
