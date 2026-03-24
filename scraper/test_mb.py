import json
import urllib.parse

urls = [
# Whey Protein Products:
"https://wellbeingnutrition.com/products/whey-protein-isolate-dark-chocolate",
"https://wellbeingnutrition.com/products/whey-protein-isolate-dark-chocolate-2kg",
"https://wellbeingnutrition.com/products/raw-whey-protein-isolate-unflavored",
"https://wellbeingnutrition.com/products/whey-protein-isolate-unflavoured-2kg",
"https://wellbeingnutrition.com/products/whey-protein-concentrate-unflavored",
"https://wellbeingnutrition.com/products/whey-protein-blend-mango-flavored",
"https://wellbeingnutrition.com/products/whey-protein-isolate-bourbon-vanilla",
"https://wellbeingnutrition.com/products/whey-protein-blend-swiss-chocolate",
"https://wellbeingnutrition.com/products/whey-protein-blend-cappuccino",
# Vegan/Plant Protein Products:
"https://wellbeingnutrition.com/products/vegan-protein-canadian-mixed-berry",
"https://wellbeingnutrition.com/products/vegan-protein-belgian-dark-chocolate-probiotics",
"https://wellbeingnutrition.com/products/vegan-protein-french-vanilla-caramel-copy",
"https://wellbeingnutrition.com/products/vegan-protein-belgian-chocolate",
"https://wellbeingnutrition.com/products/vegan-protein-french-vanilla-caramel",
"https://wellbeingnutrition.com/products/vegan-protein-italian-cafe-mocha",
"https://wellbeingnutrition.com/products/vegan-protein-flavor-combo",
"https://wellbeingnutrition.com/products/superfood-plant-protein-powder-in-banoffee-pie",
"https://wellbeingnutrition.com/products/superfood-plant-protein-powder-for-women",
"https://wellbeingnutrition.com/products/vegan-protein-dark-chocolate-hazelnut",
# Protein + Creatine Combos:
"https://wellbeingnutrition.com/products/whey-protein-isolate-dark-chocolate-creatine-monohydrate-combo",
"https://wellbeingnutrition.com/products/unflavored-whey-protein-concentrate-creatine-monohydrate-combo",
"https://wellbeingnutrition.com/products/unflavored-whey-protein-isolate-creatine-monohydrate-combo",
"https://wellbeingnutrition.com/products/whey-protein-swiss-chocolate-creatine-monohydrate-combo",
"https://wellbeingnutrition.com/products/whey-protein-cappuccino-creatine-monohydrate-combo"
]

products = []
for u in urls:
    handle = urllib.parse.urlparse(u).path.split('/')[-1]
    name = " ".join([w.capitalize() for w in handle.replace('-', ' ').split()])
    products.append({
        "product_id": f"wbn-{handle}",
        "name": name,
        "url": u
    })

with open('scraper/data/brands.json', 'r') as f:
    brands = json.load(f)

# check if wellbeing exists
found = False
for b in brands:
    if b['brand_id'] == 'wellbeingnutrition':
        b['products'] = products
        found = True
        break
        
if not found:
    brands.append({
        "brand_id": "wellbeingnutrition",
        "brand_name": "Wellbeing Nutrition",
        "base_url": "https://wellbeingnutrition.com/",
        "products": products
    })

with open('scraper/data/brands.json', 'w') as f:
    json.dump(brands, f, indent=2)
print("Updated brands.json successfully.")
